tmp="app_fixed.tmp"

# 1. Write gevent monkey patch at top
echo "from gevent import monkey" > $tmp
echo "monkey.patch_all()" >> $tmp
echo "" >> $tmp

# 2. Copy rest of app_full.py except old monkey patches and server block
skip=0
while IFS= read -r line; do
    if [[ "$line" == *"if __name__ == \"__main__\""* ]]; then
        skip=1
    fi
    if [[ $skip -eq 0 ]]; then
        echo "$line" >> $tmp
    fi
done < app_full.py

# 3. Append clean gevent server block
cat >> $tmp << 'EOR'

# ==========================================================
# CLEAN FINAL SERVER START (GEVENT) — MACOS SAFE
# ==========================================================
if __name__ == "__main__":
    print("\n=== LOLA SERVER STARTED (GEVENT) ===\n")

    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler

    http_server = WSGIServer(("0.0.0.0", PORT), app, handler_class=WebSocketHandler)
    print(f"Serving on http://0.0.0.0:{PORT}")
    http_server.serve_forever()
EOR

mv $tmp app_full.py
echo "✔ app_full.py patched for GEVENT."
