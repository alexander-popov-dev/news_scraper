import requests

from server.settings import TELEGRAM_BOT, TELEGRAM_CHANNEL


class TelegramManager:

    @staticmethod
    def send_message(message: str):
        if TELEGRAM_BOT and TELEGRAM_CHANNEL:
            url = f'https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage'
            payload = {
                'chat_id': TELEGRAM_CHANNEL,
                'text': message,
                'parse_mode': 'html',
                'link_preview_options': {'is_disabled': True},
            }

            response = requests.post(url, json=payload)

            if response.status_code != 200:
                payload['text'] = f'<code>Unable to send work. {response.text}</code>'
                requests.post(url, json=payload)
