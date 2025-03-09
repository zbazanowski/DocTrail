# 🚀 DocTrail - Setup Guide for macOS

This guide explains how to set up **DocTrail** with `launchd` on macOS.

---

## 📂 Step 1 - Check the Folder Structure
Your `DocTrail` project should look like this:
```
~/DocTrail/
├── Projects/                     # Active working files
├── TrackedHistory/               # Historical versions (managed by DocTrail)
├── Admin/                        # Logs and admin files
├── versioning_script.py          # Main script
├── de.bazanowski.doctrail.plist  # launchd agent
```

---

## ⚙️ Step 2 - Configure `de.bazanowski.doctrail.plist`
Edit the `plist` to point to your actual file locations and email. Example:
```xml
<string>/usr/bin/python3</string>
<string>/Users/your-username/DocTrail/versioning_script.py</string>
<string>/Users/your-username/DocTrail/Projects</string>
<string>/Users/your-username/DocTrail/TrackedHistory</string>
<string>/Users/your-username/DocTrail/Admin</string>
<string>your@email.com</string>
```

Make sure all paths are **fully qualified** (no `~` shorthand).

---

## 📥 Step 3 - Install the `plist`
Copy the file into the correct folder:

```sh
mkdir -p ~/Library/LaunchAgents
cp de.bazanowski.doctrail.plist ~/Library/LaunchAgents/
```

---

## 🚀 Step 4 - Load the Agent
Tell `launchd` to start monitoring:

```sh
launchctl load ~/Library/LaunchAgents/com.example.doctrail.plist
```

---

## ✅ Step 5 - Check Status
```sh
launchctl list | grep doctrail
```

You should see `de.bazanowski.doctrail.plist` in the list.

---

## 🛠️ Troubleshooting
If the agent fails, check its logs here:

```sh
cat ~/Library/Logs/de.bazanowski.doctrail.log
```

```sh
more ./Admin/version_log.md
```

---

## ⛔ To Unload/Stop the Agent
If you want to stop DocTrail:

```sh
launchctl unload ~/Library/LaunchAgents/com.example.doctrail.plist
```

---

## 🔄 Manual (ad-hoc) Testing
You can always run DocTrail manually to check changes:

```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --consistency-scan
```

---

## 📧 Email Alerts
Ensure local email sending works (Postfix) or modify to use Gmail SMTP.

---

## 💬 Questions?
If you encounter issues, feel free to ask for help or open an issue if you're using this from GitHub.

---
