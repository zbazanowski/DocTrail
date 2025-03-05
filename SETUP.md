
# 🚀 DocTrail - Setup Guide for macOS

This guide helps you configure DocTrail to run automatically using `launchd`.

---

## 📂 Step 1 - Place DocTrail Files
Ensure your DocTrail project is organized like this:

```
~/DocTrail/
├── Projects/                  # Your documents go here
├── Admin/                      # Log files go here
├── versioning_script.py        # The main script
├── com.example.doctrail.plist  # The launchd agent file
```

---

## ⚙️ Step 2 - Configure the `plist`
Edit `com.example.doctrail.plist` to point to your actual file locations and email. Example:

```xml
<string>/usr/bin/python3</string>
<string>/Users/your-username/DocTrail/versioning_script.py</string>
<string>/Users/your-username/DocTrail/Projects</string>
<string>/Users/your-username/DocTrail/Admin</string>
<string>your@email.com</string>
```

Make sure all paths are **fully qualified** (no `~` shorthand).

---

## 📁 Step 3 - Install the `plist`
Copy the file into the correct folder:

```sh
mkdir -p ~/Library/LaunchAgents
cp com.example.doctrail.plist ~/Library/LaunchAgents/
```

---

## 🚀 Step 4 - Load the Agent
Tell `launchd` to start monitoring:

```sh
launchctl load ~/Library/LaunchAgents/com.example.doctrail.plist
```

---

## ✅ Step 5 - Confirm It's Running
To check the status:

```sh
launchctl list | grep doctrail
```

You should see `com.example.doctrail` in the list.

---

## 🔄 Step 6 - Test Manually (Optional)
You can always run DocTrail manually to check:

```sh
python3 versioning_script.py ./Projects ./Admin your@email.com
```

---

## 🛠️ Step 7 - Troubleshooting
If the agent fails, check its logs here:

```sh
cat ~/Library/Logs/com.example.doctrail.log
```

---

## ⛔ To Unload/Stop the Agent
If you want to stop DocTrail:

```sh
launchctl unload ~/Library/LaunchAgents/com.example.doctrail.plist
```

---

## 📧 Email Alerts
For email alerts to work, your Mac needs to be able to send email from the terminal.

- If you want **Gmail SMTP** (or another provider) instead of the local Postfix, I can modify the script for you.
- Just let me know if you want that customization.

---

## 💬 Questions?
If you encounter issues, feel free to ask for help or open an issue if you're using this from GitHub.

---
