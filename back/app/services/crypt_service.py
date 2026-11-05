import os

from cryptography.fernet import Fernet, InvalidToken
from config import LLM_MASTER_KEY as master_key
from exceptions import DecryptException

if not master_key:
    raise RuntimeError("LLM_MASTER_KEY environment variable not set.")

fernet = Fernet(master_key.encode() if isinstance(master_key, str) else master_key)

def encrypt_secret(secret: str) -> str:
    token = fernet.encrypt(secret.encode('utf8'))
    return token.decode('utf8')

def decrypt_secret(token: str) -> str:
    try:
        secret = fernet.decrypt(token.encode('utf8'))
        return secret.decode('utf8')
    except InvalidToken:
        raise DecryptException(
            message="Cannot decrypt LLM api key", 
            status_code=500,
            )
