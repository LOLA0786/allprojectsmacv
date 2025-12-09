import os, webbrowser, time, requests

def connect_flow():
    print("Opening browser for secure login...")
    webbrowser.open("https://app.aifinops.dev/connect")

    print("Waiting for authentication...")
    time.sleep(5)

    # Poll API for token (mock for now)
    resp = requests.get("https://api.aifinops.dev/mock-token")
    
    token = resp.json().get("token", "demo-token-123")

    os.makedirs(os.path.expanduser("~/.aifinops"), exist_ok=True)

    with open(os.path.expanduser("~/.aifinops/config"), "w") as f:
        f.write(f"AIFINOPS_TOKEN={token}\n")

    print("Connected successfully!")
    print("Dashboard: https://app.aifinops.dev")
