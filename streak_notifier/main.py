import os
import random
from dotenv import load_dotenv
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import date

def load_env():
    load_dotenv()
    return {
        "GITHUB_USERNAME": os.getenv("GITHUB_USERNAME"),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "EMAIL": os.getenv("EMAIL"),
        "APP_PASSWORD": os.getenv("APP_PASSWORD"),
        "TO_EMAIL": os.getenv("TO_EMAIL", os.getenv("EMAIL")),
    }

def get_github_contribution(username, token):
    query = f"""
    {{
      user(login: "{username}") {{
        contributionsCollection {{
          contributionCalendar {{
            weeks {{
              contributionDays {{
                date
                contributionCount
              }}
            }}
          }}
        }}
      }}
    }}
    """
    res = requests.post(
        "https://api.github.com/graphql",
        json={'query': query},
        headers={"Authorization": f"Bearer {token}"}
    )
    return res.json()


def committed_today(data):
    today = str(date.today())
    for week in data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for day in week["contributionDays"]:
            if day["date"] == today:
                return day["contributionCount"] > 0
    print(committed_today(data))
    return False


def send_email(email, app_password, to_email, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as server:
        server.login(email, app_password)
        server.send_message(msg)


def main():
    config = load_env()

    quotes = [
        "Commit today, your future self will thank you!",
        "Small progress is still progress.",
        "Consistency beats intensity.",
        "Code something small, but code today!",
    ]
    motivation = random.choice(quotes)

    data = get_github_contribution(config["GITHUB_USERNAME"], config["GITHUB_TOKEN"])
    if not committed_today(data):
        send_email(
            config["EMAIL"],
            config["APP_PASSWORD"],
            config["TO_EMAIL"],
            "⚠️ Don't lose your GitHub streak!",
            f"You haven’t committed yet today.\n\n💬 {motivation}"
        )
    else:
        send_email(
            config["EMAIL"],
            config["APP_PASSWORD"],
            config["TO_EMAIL"],
            "🦾🦾🦾🦾 you irony",
            f"You have committed today hena!!! .\n\n💬 {motivation}"
        )     
    print("📩 Reminder email sent — go commit!")
    print(committed_today(data))



if __name__ == "__main__":
    main()
