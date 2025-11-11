import os
import platform
from pathlib import Path
from streak_notifier.main import main


class NotifierScheduler:
    def __init__(self, script_name="main.py", time="11:30"):
        self.script_path = Path(__file__).parent / script_name
        self.time = time
        self.os_type = platform.system()

    def _schedule_cron(self):
        user_crontab = os.popen("crontab -l 2>/dev/null").read()
        hour, minute = self.time.split(":")
        cron_job = f"{int(minute)} {int(hour)} * * * python3 {self.script_path} # github-streak-notifier\n"

        if cron_job not in user_crontab:
            os.system(f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -')
            print(f"Cron job scheduled at {self.time} daily.")
        else:
            print("Cron job already exists.")

    def _remove_cron(self):
        cron = os.popen("crontab -l 2>/dev/null").read()
        cron = "\n".join(
            [line for line in cron.splitlines() if "# github-streak-notifier" not in line]
        )
        os.system(f'echo "{cron}" | crontab -')
        print("Cron job removed.")

    def _schedule_windows(self):
        hour, minute = self.time.split(":")
        task_name = "GitHubStreakNotifier"
        os.system(
            f'schtasks /create /tn "{task_name}" /tr "python {self.script_path}" /sc daily /st {hour}:{minute} /f'
        )
        print(f"Windows Task '{task_name}' scheduled at {self.time} daily.")

    def _remove_windows_task(self):
        os.system('schtasks /delete /tn "GitHubStreakNotifier" /f')
        print("Windows Task removed.")

    def start(self):
        if self.os_type == "Windows":
            self._schedule_windows()
        elif self.os_type in ["Linux", "Darwin"]:
            self._schedule_cron()
        else:
            raise Exception("Unsupported OS")

    def stop(self):
        if self.os_type == "Windows":
            self._remove_windows_task()
        elif self.os_type in ["Linux", "Darwin"]:
            self._remove_cron()
        else:
            print("Unsupported OS")

    def run_now(self):
        main()

    def cli(self):
        print("📌 GitHub Streak Notifier Scheduler CLI")
        print("1️⃣ Start daily notifications")
        print("2️⃣ Stop daily notifications")
        print("3️⃣ Run now (check and send email)")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            self.start()
        elif choice == "2":
            self.stop()
        elif choice == "3":
            self.run_now()
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    NotifierScheduler().cli()

def cli():
    NotifierScheduler().cli()
