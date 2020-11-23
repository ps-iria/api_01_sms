import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def get_status(user_id):
    params = {
        "user_ids": user_id,
        "v": "5.126",
        "access_token": os.environ['access_token'],
        "fields": "online"
    }
    status = requests.post('https://api.vk.com/method/users.get',
                           params=params)
    status = status.json()["response"][0]["online"]
    return status


def sms_sender(sms_text):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=sms_text,
        from_=os.environ['NUMBER_FROM'],
        to=os.environ['NUMBER_TO']
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
