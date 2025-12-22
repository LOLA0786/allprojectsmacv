import json, base64, time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)

def sign_payload(payload: dict):
    data = json.dumps(payload, sort_keys=True).encode()
    signature = KEY.sign(
        data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()
