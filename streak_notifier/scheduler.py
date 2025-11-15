import os
import platform
import sys
from pathlib import Path
from streak_notifier.main import main


class NotifierScheduler:
    def __init__(self, time=None):
        self.time = time
        self.os_type = platform.system()
        # Get the full path to the Python executable
        self.python_path = sys.executable

    def _schedule_cron(self):
        user_crontab = os.popen("crontab -l 2>/dev/null").read()
        hour, minute = self.time.split(":")
        # Use full Python executable path
        command = f'"{self.python_path}" -m streak_notifier.main'
        cron_job = f"{int(minute)} {int(hour)} * * * {command} # github-streak-notifier\n"

        if cron_job not in user_crontab:
            result = os.system(f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -')
            if result == 0:
                print(f"✅ Cron job scheduled at {self.time} daily.")
                print(f"   Using Python: {self.python_path}")
            else:
                print(f"❌ Failed to create cron job. Error code: {result}")
        else:
            print("⚠️  Cron job already exists.")

    def _remove_cron(self):
        cron = os.popen("crontab -l 2>/dev/null").read()
        cron = "\n".join(
            [line for line in cron.splitlines() if "# github-streak-notifier" not in line]
        )
        os.system(f'echo "{cron}" | crontab -')
        print("Cron job removed.")

    def _schedule_windows(self):
        task_name = "GitHubStreakNotifier"
        
        # Create a batch file to ensure proper execution
        batch_file = os.path.expanduser("~/.streak_notifier_run.bat")
        
        # Check if we're in a virtual environment
        venv_path = os.path.dirname(os.path.dirname(self.python_path))
        is_venv = os.path.exists(os.path.join(venv_path, "Scripts", "activate.bat"))
        
        with open(batch_file, "w") as f:
            f.write("@echo off\n")
            if is_venv:
                # If in venv, activate it first
                f.write(f'call "{os.path.join(venv_path, "Scripts", "activate.bat")}"\n')
            f.write(f'"{self.python_path}" -m streak_notifier.main\n')
        
        # Schedule the batch file instead of direct Python command
        result = os.system(
            f'schtasks /create /tn "{task_name}" /tr "\"{batch_file}\"" /sc daily /st {self.time} /f'
        )
        if result == 0:
            print(f"✅ Windows Task '{task_name}' scheduled at {self.time} daily.")
            print(f"   Using Python: {self.python_path}")
            print(f"   Batch file: {batch_file}")
        else:
            print(f"❌ Failed to create scheduled task. Error code: {result}")

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
        print("1️⃣  Start daily notifications")
        print("2️⃣  Stop daily notifications")
        print("3️⃣  Run now (check and send email)")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            time_input = input(
                "Enter the time to send notifications (in HH:MM format, e.g., 14:30): "
            )
            try:
                hour, minute = map(int, time_input.split(":"))
                if not (0 <= hour < 24 and 0 <= minute < 60):
                    raise ValueError
                self.time = time_input
                self.start()
            except ValueError:
                print("❌ Invalid time format. Please use HH:MM (24-hour format).")
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
