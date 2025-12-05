#!/usr/bin/env bash
for i in 1 2 3 4; do
  curl -s -X POST http://127.0.0.1:7860/api/stream_intent -H "Content-Type: application/json" \
    -d "{\"user\":\"simuser$i\",\"text\":\"Looking to buy MacBook Air M2 for ML\"}" >/dev/null &
  sleep 0.4
done
echo "Simulated 4 users posting intents."
