import os
from dotenv import set_key, load_dotenv
import signal

# Store .env in user's home directory for consistent access
ENV_FILE = os.path.expanduser("~/.streak_notifier.env")

def configure_credentials():
    if not os.path.exists(ENV_FILE):
        open(ENV_FILE, "w").close()

    load_dotenv(ENV_FILE)

    credentials = {
        "GITHUB_USERNAME": input("Enter your GitHub username: "),
        "GITHUB_TOKEN": input("Enter your GitHub token: "),
        "EMAIL": input("Enter your email address: "),
        "APP_PASSWORD": input("Enter your email app password: "),
        "TO_EMAIL": input("Enter recipient email (press enter to use same email): ")
    }

    if not credentials["TO_EMAIL"]:
        credentials["TO_EMAIL"] = credentials["EMAIL"]

    for key, value in credentials.items():
        set_key(ENV_FILE, key, value)

    print(f"✅ Credentials saved successfully to {ENV_FILE}")
    print("You only need to do this once.")



PID_FILE = os.path.expanduser("~/.streak_notifier.pid")
def stop_notifier():
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            pid = int(f.read())
        os.kill(pid, signal.SIGTERM)
        os.remove(PID_FILE)
        print("Streak Notifier stopped.")
    else:
        print("No running Streak Notifier found.")
