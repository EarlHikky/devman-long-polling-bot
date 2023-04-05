import telegram
import requests
import os
import argparse
import textwrap
import time
from datetime import datetime
from requests.exceptions import ReadTimeout, ConnectionError
from dotenv import load_dotenv


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Запуск Long Polling')
    parser.add_argument("telegram_chat_id", help="id чата в Telegram")
    telegram_chat_id = parser.parse_args().telegram_chat_id
    bot = telegram.Bot(token=os.environ["TELEGRM_BOT_API_TOKEN"])
    get_lesson_status_request(bot, telegram_chat_id)


def get_lesson_status_request(bot, telegram_chat_id):
    """Get a response from Devman API."""
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": os.environ["DEVMAN_API_TOKEN"]}
    timestamp = datetime.now().timestamp()
    while True:
        try:
            payload = {"timestamp": timestamp}
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            lesson_review_data = response.json()
            if lesson_review_data["status"] == "found":
                send_message(bot, lesson_review_data, telegram_chat_id)
                timestamp = lesson_review_data["last_attempt_timestamp"]
                continue
            timestamp = lesson_review_data["timestamp_to_request"]

        except ConnectionError as error:
            print(error)
            time.sleep(60)

        except ReadTimeout:
            continue


def send_message(bot, lesson_review_data, telegram_chat_id):
    """Send a message to Telegram."""
    _lesson_review_data = lesson_review_data["new_attempts"][0]
    lesson_title = _lesson_review_data["lesson_title"]
    status = ("Not OK" if _lesson_review_data["is_negative"] else "OK")
    lesson_url = _lesson_review_data['lesson_url']
    message = f"""
                Преподаватель проверил работу!
                {lesson_title}: {status}
                {lesson_url}
                """
    bot.send_message(text=textwrap.dedent(message), chat_id=telegram_chat_id)


if __name__ == '__main__':
    main()
