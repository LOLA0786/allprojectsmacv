# Create new fixed file
tmp="app_fixed.tmp"

# 1. Write eventlet monkey_patch immediately at top
echo "import eventlet" > $tmp
echo "eventlet.monkey_patch()" >> $tmp
echo "" >> $tmp

# 2. Append rest of app_full.py BUT SKIP any existing monkey_patch or old server block
skip=0
while IFS= read -r line; do
    # Skip old server blocks
    if [[ "$line" == *"if __name__ == \"__main__\""* ]]; then
        skip=1
    fi
    if [[ $skip -eq 0 ]]; then
        echo "$line" >> $tmp
    fi
done < app_full.py

# 3. Append clean final server run block
cat >> $tmp << 'EOR'

# ==========================================================
# CLEAN FINAL SERVER START (EVENTLET)
# ==========================================================
if __name__ == "__main__":
    print("\n=== LOLA SERVER STARTED (EVENTLET) ===\n")

    from eventlet import wsgi
    import eventlet

    listener = eventlet.listen(("0.0.0.0", PORT))
    wsgi.server(listener, app)
EOR

# Replace original file
mv $tmp app_full.py
echo "✔ app_full.py repaired successfully."
