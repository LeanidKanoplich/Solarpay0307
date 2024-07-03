import os
import json
from typing import List
import tempfile
import uuid
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OUTPUT_DIR = os.path.join(
    tempfile.gettempdir(),
    'openai_telegram',
    'audios'
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

TOKEN = os.getenv('TOKEN')
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'

def send_message(chat_id: int, message: str) -> bool:
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/sendMessage', json=payload, headers=headers)
    status_code = response.status_code
    response = json.loads(response.text)

    return status_code == 200 and response['ok']

def send_photo(chat_id: int, url: str, caption: str = '') -> bool:
    payload = {
        'chat_id': chat_id,
        'photo': url
    }

    if caption:
        payload['caption'] = caption

    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/sendPhoto', json=payload, headers=headers)
    status_code = response.status_code
    response = json.loads(response.text)

    return status_code == 200 and response['ok']

def set_webhook(url: str, secret_token: str = '') -> bool:
    payload = {'url': url}

    if secret_token:
        payload['secret_token'] = secret_token

    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/setWebhook', json=payload, headers=headers)
    print(response.text)
    status_code = response.status_code
    response = json.loads(response.text)

    return status_code == 200 and response['ok']

def set_menu_commands(commands: List[dict]) -> bool:
    payload = {'commands': commands}

    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/setMyCommands', json=payload, headers=headers)
    status_code = response.status_code
    response = json.loads(response.text)

    return status_code == 200 and response['ok']

def get_file_path(file_id: str) -> dict:
    url = f'{BASE_URL}/getFile'
    querystring = {'file_id': file_id}
    response = requests.request('GET', url, params=querystring)

    if response.status_code == 200:
        data = json.loads(response.text)
        file_path = data['result']['file_path']

        return {
            'status': 1,
            'file_path': file_path
        }
    else:
        return {
            'status': 0,
            'file_path': ''
        }

def save_file_and_get_local_path(file_path: str) -> dict:
    url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    response = requests.request('GET', url)
    extension = file_path.split('.')[-1]
    file_id = uuid.uuid1()
    file_name = f'{file_id}.{extension}'
    local_file_path = os.path.join(
        OUTPUT_DIR,
        file_name
    )

    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)

        return {
            'status': 1,
            'local_file_path': local_file_path,
            'file_name': file_name,
            'file_id': file_id,
            'extension': extension
        }
    else:
        return {
            'status': 0,
            'local_file_path': '',
            'file_name': '',
            'file_id': '',
            'extension': ''
        }

def send_audio(chat_id: int, url: str, caption: str = '') -> bool:
    payload = {
        'chat_id': chat_id,
        'audio': url
    }

    if caption:
        payload['caption'] = caption

    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        'POST', f'{BASE_URL}/sendAudio', json=payload, headers=headers)
    status_code = response.status_code
    response = json.loads(response.text)

    return status_code == 200 and response['ok']

def save_audio(file_id, file_path):
    try:
        file_content = download_file_from_telegram(file_id)

        with open(file_path, 'wb') as f:
            f.write(file_content)

        if os.path.exists(file_path):
            print("File saved successfully.")
        else:
            print("File save failed.")
    except Exception as e:
        print(f"Error saving file: {e}")

def download_file_from_telegram(file_id):
    file_info = get_file_path(file_id)
    if file_info['status'] == 1:
        file_path = file_info['file_path']
        url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
        response = requests.request('GET', url)
        if response.status_code == 200:
            return response.content
    return None

def handle_telegram_update(update):
    try:
        query = None

        if 'message' in update:
            message = update['message']
            if 'voice' in message:
                file_id = message['voice']['file_id']
                file_path = os.path.join(OUTPUT_DIR, f"{file_id}.ogg")
                save_audio(file_id, file_path)

                query = transcribe_audio(file_path)

                respond_to_telegram(query)
        else:
            print("No message found in update.")
    except Exception as e:
        print(f"Error at telegram...\n{e}")

def transcribe_audio(file_path):
    # Логика транскрипции аудио файла
    pass

def respond_to_telegram(query):
    # Логика отправки ответа в Telegram
    pass
