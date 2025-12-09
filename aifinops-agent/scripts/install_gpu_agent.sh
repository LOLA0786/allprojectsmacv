#!/bin/bash
echo "Installing GPU agent..."
pip install pynvml requests || true
echo "Agent installed (simulated)."
