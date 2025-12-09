import os, webbrowser, time
def connect_flow():
    print("Opening login...")
    try: webbrowser.open("https://app.aifinops.dev/connect")
    except: print("Open manually.")
    time.sleep(2)
    token="demo-token-123"
    os.makedirs(os.path.expanduser("~/.aifinops"), exist_ok=True)
    with open(os.path.expanduser("~/.aifinops/config"), "w") as f:
        f.write(f"AIFINOPS_TOKEN={token}\n")
    print("Done! Token saved.")
