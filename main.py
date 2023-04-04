import telegram
import requests
import json
import os
from requests.exceptions import ReadTimeout, ConnectionError
from dotenv import load_dotenv
import argparse
import textwrap
import time


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Запуск Long Polling')
    parser.add_argument("telegram_chat_id", help="id чата в Telegram")
    telegram_chat_id = parser.parse_args().telegram_chat_id
    bot = telegram.Bot(token=os.environ["TELEGRM_BOT_API_TOKEN"])
    get_lesson_status_request(bot, telegram_chat_id)


def get_lesson_status_request(bot, telegram_chat_id):
    """Get a respomse from Devman API."""
    headers = {"Authorization": os.environ["DEVMAN_API_TOKEN"]}
    while True:
        try:
            url = "https://dvmn.org/api/long_polling/"
            response = requests.get(url, headers=headers, timeout=2)
            response.raise_for_status()
            response_data = json.loads(response.text)
            if response_data["status"] == "found":
                send_message(bot, response_data, telegram_chat_id)
                headers.update(timestamp=str(response_data["last_attempt_timestamp"]))
                continue
            headers.update(timestamp=str(response_data["timestamp_to_request"]))

        except ConnectionError as error:
            print(error)
            time.sleep(60)

        except ReadTimeout:
            continue


def send_message(bot, response_data, telegram_chat_id):
    """Send a message to Telegram."""
    _response_data = response_data["new_attempts"][0]
    lesson_title = _response_data["lesson_title"]
    status = ("Not OK" if _response_data["is_negative"] else "OK")
    lesson_url = _response_data['lesson_url']
    message = f"""
                Преподаватель проверил работу!
                {lesson_title}: {status}
                {lesson_url}
                """
    bot.send_message(text=textwrap.dedent(message), chat_id=telegram_chat_id)


if __name__ == '__main__':
    main()
