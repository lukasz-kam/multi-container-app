import os
import requests
from dotenv import dotenv_values
from base64 import b64encode
from nacl import encoding, public

secrets = dotenv_values("../.env")
gh_config = dotenv_values("../.gh_token")

GITHUB_TOKEN = gh_config.get('GITHUB_TOKEN', "")
REPO_NAME = 'lukasz-kam/multi-container-app'
API_URL = f'https://api.github.com/repos/{REPO_NAME}/actions/secrets'

def get_github_public_key():
    url = f'https://api.github.com/repos/{REPO_NAME}/actions/secrets/public-key'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(response.json())
    return response.json()

def encrypt_secret(secret_value, public_key):
    public_key_str = public_key.get('key', '')
    public_key = public.PublicKey(public_key_str.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

    return b64encode(encrypted).decode("utf-8")

def set_github_secret(secret_name, secret_value, public_key):
    encrypted_value = encrypt_secret(secret_value, public_key)
    url = f'{API_URL}/{secret_name}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    payload = {
        'encrypted_value': encrypted_value,
        'key_id': public_key['key_id'],
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 201:
        print(f'Successfully set secret: {secret_name}')
    else:
        print(f'Error setting secret: {response.text}')

def upload_secrets_to_github():
    public_key = get_github_public_key()
    for secret_name, secret_value in secrets.items():
        set_github_secret(secret_name, secret_value, public_key)

if __name__ == "__main__":
    upload_secrets_to_github()
