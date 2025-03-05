
# 📚 DocTrail - Automatic Document Versioning System

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux-lightgrey)
![Status](https://img.shields.io/badge/Status-Development-yellow)

## 🌟 Overview
**DocTrail** is a lightweight and flexible **versioning automation tool** for managing annotated documents (PDFs, DOCX, TXT, and more).  
It automatically tracks changes to files stored in your **Projects folder**, keeping **time-stamped historical versions** in hidden folders next to each file.

---

## 🚀 Features
✅ Works for any file type you configure (PDF, DOCX, TXT, etc.)  
✅ Auto-detects changes and versions files without user interaction  
✅ Keeps historical versions in hidden folders next to each file  
✅ Maintains a **global log** for audit trail  
✅ Detects missing history folders and can auto-rebuild them  
✅ Optional **email alerts** on error conditions  
✅ Compatible with **iCloud Drive** or other cloud-synced storage  

---

## 📁 Folder Structure
```
Projects/
├── Project_A/
│   ├── Document_1.pdf
│   ├── .document_1_pdf/           # Hidden folder with history versions
│   ├── Document_2.docx
│   ├── .document_2_docx/
├── Project_B/
│   ├── Notes.md
Admin/
├── version_log.md                  # Global versioning log
```

---

## 📥 Installation
### 1. Clone the Repo
```sh
git clone https://github.com/your-username/doctrail.git
cd doctrail
```

### 2. Set Up Python
- Recommended: **Python 3.9 or newer**
- Create Virtual Environment (optional but recommended)
```sh
python3 -m venv venv
source venv/bin/activate
```

---

## ▶️ Usage
### Full Scan (all files in all projects)
```sh
python3 versioning_script.py ./Projects ./Admin your@email.com
```

### Scan Single File
```sh
python3 versioning_script.py ./Projects ./Admin your@email.com --scan-file "./Projects/Project_A/Document_1.pdf"
```

### Force Rescan All Files (ignore existing hashes)
```sh
python3 versioning_script.py ./Projects ./Admin your@email.com --rescan-all
```

### Rebuild Missing History Folders
```sh
python3 versioning_script.py ./Projects ./Admin your@email.com --rebuild-folders
```

---

## ⚙️ Automation (Optional for macOS)
Create a `launchd` agent to run the script every hour (sample plist is included in the repo).

1. Copy `com.example.doctrail.plist` into:
```
~/Library/LaunchAgents/
```
2. Edit file paths and email inside the plist.
3. Load the agent:
```sh
launchctl load ~/Library/LaunchAgents/com.example.doctrail.plist
```

---

## ✅ Supported File Types
You can easily extend this list in the script:
- PDF
- DOCX
- TXT
- XLSX
- PPTX
- MD
- CSV
- PNG
- JPG

---

## 📧 Email Notifications
DocTrail can send email alerts if something goes wrong (like missing extensions, etc.).  
By default, it tries sending via `localhost` SMTP (e.g., Postfix).  
**You can modify the script to use Gmail SMTP or any external provider if preferred.**

---

## 📊 Future Enhancements (Ideas)
- [ ] Add support for cloud storage APIs (Google Drive, Dropbox metadata integration)
- [ ] Add GitHub Actions for CI testing
- [ ] Add Dockerfile for containerized deployment (optional for servers)

---

## 💬 Questions or Feedback?
Feel free to open an [issue](https://github.com/your-username/doctrail/issues) if you encounter problems or have suggestions.

---

## ⚠️ Disclaimer
This is **not an official product** — use at your own risk.  
Designed for tech-savvy users comfortable with Python and terminal operations.

---

## 📝 License
Apache License 2.0

---

## 👨‍💻 Author
Developed with ❤️ by [Your Name or GitHub Username]

---

## 📌 Quick Link
[👉 View the Script](versioning_script.py)
