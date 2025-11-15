# 🔥 GitHub Streak Notifier

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Never lose your GitHub contribution streak again! This automated tool checks your daily GitHub contributions and sends you smart email notifications to keep you motivated and consistent.

## 🎯 What Does It Do?

GitHub Streak Notifier is a lightweight Python package that:
- 🔍 **Monitors** your GitHub contribution activity daily
- 📧 **Sends motivational emails** when you haven't committed yet
- 🎉 **Celebrates with you** when you've already contributed
- ⏰ **Runs automatically** at your preferred time using system schedulers
- 🌍 **Works everywhere** - Windows, macOS, and Linux

Perfect for developers who want to maintain their green contribution graph without checking GitHub manually every day!

## ✨ Key Features

- **🤖 Automated Daily Checks**: Set it once, and it runs automatically every day
- **📨 Smart Email Notifications**:
  - Motivational reminders if you haven't contributed yet
  - Congratulatory messages when you have contributed
- **⏰ Customizable Schedule**: Choose exactly when you want to receive notifications (24-hour format)
- **🔒 Secure**: Credentials stored locally in your home directory
- **🪶 Lightweight**: Minimal dependencies and resource usage
- **🖥️ Cross-Platform**: Native integration with Windows Task Scheduler and Unix cron
- **📝 Debug Logs**: Built-in logging to troubleshoot any issues

## 📋 Prerequisites

Before installing, make sure you have:

- **Python 3.8 or higher** installed on your system
- **pip** (Python package installer)
- A **Gmail account** (for sending emails)
- A **GitHub account** with a Personal Access Token

## 🚀 Installation

### Option 1: Install from Source (Recommended for Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HenokAsaye/github_streak_notifier.git
   cd github_streak_notifier
   ```

2. **Create a virtual environment (optional but recommended):**
   
   **Windows:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the package:**
   ```bash
   pip install .
   ```

### Option 2: Install from PyPI (Coming Soon)
```bash
pip install github-streak-notifier
```

### ⚠️ Windows Users: Add Scripts to PATH

After installation, if commands like `streak_notifier_start` are not recognized, add the Scripts directory to your PATH:

```powershell
$env:Path += ";$env:APPDATA\Python\Python313\Scripts"
```

Or permanently add `C:\Users\YourUsername\AppData\Roaming\Python\Python313\Scripts` to your system PATH.

## 🔧 Configuration

### Step 1: Get Your GitHub Personal Access Token

1. Go to [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Give it a name (e.g., "Streak Notifier")
4. Select the **`read:user`** scope (this allows reading your contribution data)
5. Click **Generate token** and **copy it immediately** (you won't see it again!)

### Step 2: Get Your Gmail App Password

1. Go to your [Google Account Security Settings](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select **Mail** and **Other (Custom name)**
5. Name it "GitHub Streak Notifier"
6. Click **Generate** and copy the 16-character password

### Step 3: Configure Your Credentials

Run the configuration command:

```bash
cli_configuration
```

You'll be prompted to enter:
- **GitHub Username**: Your GitHub username (e.g., `HenokAsaye`)
- **GitHub Token**: The personal access token from Step 1
- **Email Address**: Your Gmail address (e.g., `your.email@gmail.com`)
- **Email App Password**: The 16-character app password from Step 2
- **Recipient Email**: Where to receive notifications (press Enter to use the same email)

Your credentials are securely saved to `~/.streak_notifier.env` in your home directory.

## 📖 Usage

### Starting the Scheduler

Run the interactive scheduler:

```bash
streak_notifier_start
```

You'll see a menu:

```
📌 GitHub Streak Notifier Scheduler CLI
1️⃣  Start daily notifications
2️⃣  Stop daily notifications
3️⃣  Run now (check and send email)
Enter your choice (1/2/3):
```

### Option 1: Schedule Daily Notifications

1. Choose option **1**
2. Enter your preferred time in **24-hour format** (e.g., `09:00` for 9 AM, `21:30` for 9:30 PM)
3. The tool will create a scheduled task that runs automatically every day

**Examples:**
- `07:00` - 7:00 AM
- `12:00` - 12:00 PM (noon)
- `18:30` - 6:30 PM
- `23:00` - 11:00 PM

### Option 2: Stop Daily Notifications

Choose option **2** to remove the scheduled task and stop receiving notifications.

### Option 3: Run Immediately

Choose option **3** to check your GitHub streak and send an email right now (useful for testing).

### Manual Run (Alternative)

You can also run a check manually anytime:

```bash
streak_notifier
```

## 🛠️ Troubleshooting

### Commands Not Found

If you get `command not found` errors, ensure the Scripts directory is in your PATH:

**Windows:**
```powershell
$env:Path += ";$env:APPDATA\Python\Python313\Scripts"
```

**macOS/Linux:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Scheduled Task Not Running

1. **Check the log file** for errors:
   - Location: `~/.streak_notifier.log` (in your home directory)
   - Windows: `C:\Users\YourUsername\.streak_notifier.log`
   - macOS/Linux: `~/.streak_notifier.log`

2. **Verify the task exists:**
   
   **Windows:**
   ```powershell
   schtasks /query /tn "GitHubStreakNotifier"
   ```
   
   **macOS/Linux:**
   ```bash
   crontab -l | grep github-streak-notifier
   ```

3. **Test manually first:**
   ```bash
   streak_notifier
   ```
   If this works but the scheduled task doesn't, check the log file for clues.

### Email Not Sending

- Verify your Gmail App Password is correct (not your regular Gmail password)
- Ensure 2-Step Verification is enabled on your Google account
- Check if your credentials are properly saved: `cat ~/.streak_notifier.env`

### GitHub API Errors

- Verify your Personal Access Token has the `read:user` scope
- Check if the token has expired (regenerate if needed)

## 📁 Files Created

The tool creates these files in your home directory:

- `~/.streak_notifier.env` - Your encrypted credentials
- `~/.streak_notifier.log` - Activity and error logs
- `~/.streak_notifier_run.bat` (Windows only) - Batch file for scheduled tasks

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.py) file for details.

## 👨‍💻 Author

**Henok Asaye**
- GitHub: [@HenokAsaye](https://github.com/HenokAsaye)
- Email: henokasaye77@gmail.com

## 🙏 Acknowledgments

- Thanks to the GitHub GraphQL API for contribution data
- Motivational quotes from [ZenQuotes](https://zenquotes.io/)
- Compliments from [Complimentr](https://complimentr.com/)

## ⭐ Show Your Support

If this project helped you maintain your GitHub streak, give it a ⭐️!

---

**Happy Coding! Keep that streak alive! 🔥**