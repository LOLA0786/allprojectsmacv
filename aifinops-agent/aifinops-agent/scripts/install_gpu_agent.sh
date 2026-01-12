#!/bin/bash
echo "Installing AIFinOps GPU Agent..."

pip install pynvml requests

cat > /usr/local/bin/aifinops-gpu << 'EOA'
#!/usr/bin/env python3
import time, requests
from pynvml import *

nvmlInit()
while True:
    handle = nvmlDeviceGetHandleByIndex(0)
    util = nvmlDeviceGetUtilizationRates(handle).gpu
    mem  = nvmlDeviceGetMemoryInfo(handle)

    payload = {
        "gpu_util": util,
        "memory_used": mem.used,
        "memory_total": mem.total
    }
    requests.post("https://api.aifinops.dev/gpu", json=payload)
    time.sleep(10)
EOA

chmod +x /usr/local/bin/aifinops-gpu
echo "Run: aifinops-gpu"
