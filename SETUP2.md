
# 🚀 DocTrail - Setup Guide for macOS

This guide explains how to set up **DocTrail** with `launchd` on macOS.

---

## 📂 Folder Structure
Your `DocTrail` project should look like this:
```
~/DocTrail/
├── Projects/                    # Active working files
├── TrackedHistory/               # Historical versions (managed by DocTrail)
├── Admin/                        # Logs and admin files
├── versioning_script.py          # Main script
├── com.example.doctrail.plist    # launchd agent
```

---

## ⚙️ Configure `com.example.doctrail.plist`
Edit the plist to reflect your real paths and email:
```xml
<string>/usr/bin/python3</string>
<string>/Users/your-username/DocTrail/versioning_script.py</string>
<string>/Users/your-username/DocTrail/Projects</string>
<string>/Users/your-username/DocTrail/TrackedHistory</string>
<string>/Users/your-username/DocTrail/Admin</string>
<string>your@email.com</string>
```

---

## 📥 Install `launchd` Agent
```sh
mkdir -p ~/Library/LaunchAgents
cp com.example.doctrail.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.example.doctrail.plist
```

---

## ✅ Check Status
```sh
launchctl list | grep doctrail
```

---

## 🔄 Test Manually
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com
```

---

## 📧 Email Alerts
Ensure local email sending works (Postfix) or modify to use Gmail SMTP.

---

## 💬 Questions?
Ask or file issues in the GitHub repo.

---
