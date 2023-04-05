# Long-Polling-Bot
Получает статус работы на сайте [Devman](https://dvmn.org/)

main.py уведомляет личным сообщением в Telegram, когда работа приходит с проверки. 

## Установка
- для windows: 
 
    ```
    pip install -r requirements.txt
    ```

- для mac, linux: 

    ```
    pip3 install -r requirements.txt
    ```

## Настройка
Создать файл .env c переменными `DEVMAN_API_TOKEN=` "токен Devman API", `TELEGRM_BOT_API_TOKEN=` "токен бота Telegram".

## Запуск
- для windows: 

    ```
    python main.py "Telegram chat id"
    ``` 

- для mac, linux: 

    ```
    python3 main.py "Telegram chat id"
    ``` 

## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте Devman.
