import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import date
from dotenv import load_dotenv
import random


def load_env():
    """Load environment variables from .env file"""
    load_dotenv()
    return {
        "GITHUB_USERNAME": os.getenv("GITHUB_USERNAME"),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "EMAIL": os.getenv("EMAIL"),
        "APP_PASSWORD": os.getenv("APP_PASSWORD"),
        "TO_EMAIL": os.getenv("TO_EMAIL", os.getenv("EMAIL")),
    }


def get_github_contribution(username, token):
    """Fetch GitHub contribution data for the user"""
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

    if res.status_code != 200:
        raise Exception(f"GitHub API error: {res.status_code}, {res.text}")

    return res.json()


def committed_today(data):
    """Check if user committed today"""
    today = str(date.today())
    for week in data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for day in week["contributionDays"]:
            if day["date"] == today:
                return day["contributionCount"] > 0
    return False


def fetch_motivation():
    """Fetch random motivational quote"""
    try:
        res = requests.get("https://zenquotes.io/api/random", timeout=5)
        if res.status_code == 200:
            quote = res.json()[0]
            return f"💬 {quote['q']} — {quote['a']}"
    except Exception:
        pass
    return random.choice([
        "Small progress is still progress.",
        "Discipline is doing what needs to be done even when you don’t feel like it.",
        "Consistency beats intensity — commit today!",
        "Push something small, but push today!",
    ])


def fetch_appreciation():
    try:
        res = requests.get("https://complimentr.com/api", timeout=5)
        if res.status_code == 200:
            compliment = res.json()["compliment"]
            return f"👏 {compliment.capitalize()} Keep it up!"
    except Exception:
        pass
    return random.choice([
        "You’re on fire! 🔥 Keep that streak alive!",
        "Nice work — progress every day adds up!",
        "You did great today. Keep building your legacy! 💪",
    ])


def send_email(sender, app_password, recipient, subject, message):
    """Send email via Gmail SMTP"""
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as server:
        server.login(sender, app_password)
        server.send_message(msg)


def main():
    config = load_env()

    print("🔍 Checking your GitHub activity...")

    data = get_github_contribution(config["GITHUB_USERNAME"], config["GITHUB_TOKEN"])
    has_committed = committed_today(data)

    if not has_committed:
        message = fetch_motivation()
        subject = "⚠️ Don't lose your GitHub streak!"
    else:
        message = fetch_appreciation()
        subject = "🎉 Great job! You committed today!"

    send_email(
        config["EMAIL"],
        config["APP_PASSWORD"],
        config["TO_EMAIL"],
        subject,
        message
    )

    print("📩 Email sent successfully!")
    print("✅" if has_committed else "⚠️ You haven’t committed yet — go push something!")


if __name__ == "__main__":
    main()
