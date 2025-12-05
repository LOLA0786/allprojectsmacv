import base64
import nacl.secret
import nacl.utils
from nacl.hash import sha256

def derive_key_from_password(password: str) -> bytes:
    # Demo only: in prod use PBKDF2/HKDF with salt & many iterations
    return sha256(password.encode('utf-8'), encoder=nacl.encoding.RawEncoder)[:32]

def decrypt_secretbox(cipher_b64: str, password: str) -> str:
    raw = base64.b64decode(cipher_b64)
    nonce = raw[:24]
    ct = raw[24:]
    key = derive_key_from_password(password)
    box = nacl.secret.SecretBox(key)
    return box.decrypt(ct, nonce).decode('utf-8')
