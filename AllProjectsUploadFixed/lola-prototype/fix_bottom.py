import io

with open("app_full.py") as f:
    lines = f.readlines()

# Remove everything from last "if __name__" onward
for i, line in enumerate(lines):
    if line.strip().startswith("if __name__"):
        cut = i
        break

clean = lines[:cut]

clean.append('if __name__ == "__main__":\n')
clean.append('    print("\\n=== STARTING LOLA EVENTLET SERVER ===\\n")\n')
clean.append('    import eventlet\n')
clean.append('    eventlet.monkey_patch()\n')
clean.append('\n')
clean.append('    socketio.run(\n')
clean.append('        app,\n')
clean.append('        host="0.0.0.0",\n')
clean.append('        port=PORT,\n')
clean.append('        debug=False,\n')
clean.append('        use_reloader=False,\n')
clean.append('        allow_unsafe_werkzeug=True,\n')
clean.append('        async_mode="eventlet"\n')
clean.append('    )\n')

with open("app_full.py", "w") as f:
    f.writelines(clean)

print("✔ FIXED app_full.py bottom block.")
