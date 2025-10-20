from datetime import datetime

def log(agent, message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{agent}] {message}")
