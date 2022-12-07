import logging
from time import sleep

import requests
import telegram
from environs import Env


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot: telegram.Bot, chat_id: int):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    env = Env()
    env.read_env()

    dvmn_authorization_token = env('DVMN_AUTHORIZATION_TOKEN')
    tg_bot_api_key = env('TG_BOT_API_KEY')
    tg_chat_id = env('TG_CHAT_ID')

    bot = telegram.Bot(token=tg_bot_api_key)

    params = {}
    headers = {'Authorization': f'Token {dvmn_authorization_token}'}

    logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(message)s"
    )
    logger = logging.getLogger('tg_dvmn_alert')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(tg_bot=bot, chat_id=tg_chat_id))
    logger.warning("Бот запущен")

    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/', headers=headers, params=params)
            response.raise_for_status()
            user_reviews = response.json()

            if user_reviews['status'] == 'timeout':
                params = {
                    'timestamp': user_reviews['timestamp_to_request']
                }

            if user_reviews['status'] == 'found':
                params = {
                    'timestamp': user_reviews['last_attempt_timestamp']
                }

                for attempt in user_reviews['new_attempts']:
                    if attempt['is_negative']:
                        lesson_status = 'К сожалению в работе нашлись ошибки.'
                        lesson = f'Урок: {attempt["lesson_title"]} - {attempt["lesson_url"]}'
                        message = f'Преподаватель проверил работу.{lesson_status} {lesson}'

                        bot.send_message(chat_id=tg_chat_id, text=message)

                    else:
                        lesson_status = 'В вашей работе нет ошибок! Поздравляем!'
                        lesson = f'Урок: {attempt["lesson_title"]} - {attempt["lesson_url"]}'
                        message = f'Преподаватель проверил работу. \
                        {lesson_status} {lesson}'

                        bot.send_message(chat_id=tg_chat_id, text=message)

        except requests.exceptions.ReadTimeout:
            logger.error('Отсутсвует подключение к серверу')
            continue

        except requests.ConnectionError:
            sleep(30)
            logger.error('Ошибка подключения к серверу')


if __name__ == '__main__':
    main()
