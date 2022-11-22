import requests
from environs import Env
import telegram
from time import sleep


def main():
    env = Env()
    env.read_env()

    dvmn_authorization_token = env('DVMN_AUTHORIZATION_TOKEN')
    tg_bot_api_key = env('TG_BOT_API_KEY')
    tg_chat_id = env('TG_CHAT_ID')

    bot = telegram.Bot(token=tg_bot_api_key)

    params = {}
    headers = {'Authorization': f'Token {dvmn_authorization_token}'}

    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/', headers=headers, params=params)
            response.raise_for_status()
            user_reviews = response.json()

            print(user_reviews)

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
            continue

        except requests.ConnectionError:
            sleep(30)
            print('Ошибка подключения к серверу')


if __name__ == '__main__':
    main()
