import json, time
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

PRIVATE_KEY_PATH = "keys/policy_signing.pem"

def sign_payload(payload: dict):
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None
        )

    canonical = json.dumps(payload, sort_keys=True).encode()
    signature = private_key.sign(
        canonical,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return {
        "signature": signature.hex(),
        "signed_at": int(time.time()),
        "payload": payload
    }
