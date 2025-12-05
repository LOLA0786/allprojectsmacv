import time
import requests

API_URL = "http://0.0.0.0:8000/ingest"

def send_test_email(subject: str, body: str):
    payload = {
        "source": "gmail",
        "type": "email",
        "timestamp": int(time.time()),
        "content": f"Subject: {subject}\\n\\n{body}",
        "metadata": {"subject": subject}
    }
    r = requests.post(API_URL, json=payload, timeout=5)
    print(r.status_code, r.text)

if __name__ == "__main__":
    send_test_email("Hello from Gmail Mock", "This is a mock Gmail email containing hello keyword.")
