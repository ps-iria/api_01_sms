import os

import requests
import time
from dotenv import load_dotenv

from twilio.rest import Client

load_dotenv()


def get_status(user_id):
    params = {
        "user_id": user_id,
        "v": "5.126",
        "access_token": os.environ['access_token'],
    }
    status = requests.post('https://api.vk.com/method/status.get', params)
    status = status.json()['response']['text']
    return status  # Верните статус пользователя в ВК


def send_sms(sms_text, client):
    message = client.messages.create(
        body=sms_text,
        from_=os.environ['TWILIO_NUMBER'],
        to=os.environ['MY_NUMBER']
    )
    return message.sid  # Верните sid отправленного сообщения из Twilio


if __name__ == '__main__':
    # тут происходит инициализация Client
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == "1":
            send_sms(f'{vk_id} Поставил статус 1', client)
            break
        time.sleep(5)
