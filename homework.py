import os
from venv import logger

import requests
import time
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

URL_USERS_GET = 'https://api.vk.com/method/users.get'
VERSION_API = "5.126"
VK_TOKEN = os.environ['VK_TOKEN']
ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
NUMBER_FROM = os.environ['NUMBER_FROM']
NUMBER_TO = os.environ['NUMBER_TO']

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def get_status(user_id):
    params = {
        "user_ids": user_id,
        "v": VERSION_API,
        "access_token": VK_TOKEN,
        "fields": "online"
    }
    try:
        status = requests.post(URL_USERS_GET,
                               params=params)
        status = status.json()["response"][0]["online"]
    except Exception as e:
        logger.exception(e)
        status = e
    return status


def sms_sender(sms_text):
    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
