#!/bin/bash
set -e

echo "[1] Creating folder structure..."
mkdir -p aifinops_agent/cli
mkdir -p aifinops_agent/core
mkdir -p scripts
mkdir -p api_server

echo "[2] Writing setup.py..."
cat > setup.py << 'EOP'
from setuptools import setup, find_packages
setup(
    name="aifinops-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests","click","boto3","fastapi","uvicorn"],
    entry_points={"console_scripts":["aifinops=aifinops_agent.cli.main:cli"]},
)
EOP

echo "[3] Writing CLI..."
cat > aifinops_agent/cli/main.py << 'EOP'
import click
from aifinops_agent.core.connect import connect_flow
from aifinops_agent.core.aws_setup import setup_aws

@click.group()
def cli(): pass

@cli.command()
def connect(): connect_flow()

@cli.command()
def setup_aws_cmd(): setup_aws()
EOP

echo "[4] Writing connect flow..."
cat > aifinops_agent/core/connect.py << 'EOP'
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
EOP

echo "[5] Writing aws setup..."
cat > aifinops_agent/core/aws_setup.py << 'EOP'
def setup_aws():
    print("AWS Setup placeholder.")
EOP

echo "[6] Creating GPU installer..."
cat > scripts/install_gpu_agent.sh << 'EOP'
#!/bin/bash
echo "Installing GPU agent..."
pip install pynvml requests || true
echo "Agent installed (simulated)."
EOP
chmod +x scripts/install_gpu_agent.sh

echo "[7] Creating API server..."
mkdir -p api_server
cat > api_server/main.py << 'EOP'
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def root(): return {"status": "ok"}
EOP

echo "Bootstrap complete."
