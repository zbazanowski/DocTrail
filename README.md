
# 📚 DocTrail - Automatic Document Versioning System

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux-lightgrey)
![Status](https://img.shields.io/badge/Status-Development-yellow)

## 🌟 Overview
**DocTrail** is a lightweight and flexible **versioning automation tool** for managing annotated documents (PDFs, DOCX, TXT, and more).  
It automatically tracks changes to files stored in your **Projects folder**, keeping **time-stamped historical versions** in the separate `TrackedHistory/` folder.

---

## 🚀 Features
✅ Works for any file type you configure (PDF, DOCX, TXT, etc.)  
✅ Auto-detects changes and versions files without user interaction   
✅ Keeps historical versions in `TrackedHistory/`, separate from the working `Projects/` folder  
✅ Maintains a **global log** for audit trail  
✅ Supports multiple scan modes (flexible performance vs. precision)  
✅ Optional **email alerts** on error conditions  
✅ Compatible with **iCloud Drive, OneDrive, Dropbox**, etc.  


---

## 📂 Folder Structure
```
Projects/                     # Your active working files
├── Project_A/
│   ├── Document_1.pdf
│   ├── Document_2.docx
├── Project_B/
│   ├── Notes.md

TrackedHistory/               # Automatically maintained historical versions
├── .Project_A/
│   ├── .document_1_pdf/      # History versions of Document_1.pdf
│   ├── .document_2_docx/     # History versions of Document_2.docx
├── .Project_B/
│   ├── .notes_md/            # History versions of Notes.md

Admin/                        # Logs and admin files
├── version_log.md            # Global versioning log
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

## ▶️ Usage Examples

### Full Scan (all files in all projects - default mtime (modification time) scan)
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com
```

### Full Scan based on Hash
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --hash-scan
```

### Force New Version for Each File
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --force-version
```

### Force New Version for a Single File  (irrespective of hash and mtime)
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --force-version --scan-file "./Projects/Project_A/Document_1.pdf"
```

### Consistency Check
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --consistency-scan
```

### Disable Email Notifications
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --no-email
```

### Check Logs
```sh
more ./Admin/version_log.md
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
- PDF, DOCX, TXT, XLSX, PPTX, MD, CSV, PNG, JPG

---

## 📧 Email Notifications
DocTrail can send email alerts if something goes wrong (like missing extensions, etc.).  
By default, it tries sending via `localhost` SMTP (e.g., Postfix).  
**You can modify the script to use Gmail SMTP or any external provider if preferred.**

---

## 📊 Future Enhancements (Ideas)
- [ ] Add LICENCE.md
- [ ] Consolidate timezones
- [ ] Add the original name of the backed-up file, its file size, and full details of the current and the last version to hash.json
- [ ] Polish up the parsing code
- [ ] Add --analysis-scan (categorize files into UP-TO-DATE, UPDATED, INCOSTENT)
- [ ] Improve the command line logic for email support
- [ ] Add support for cloud storage APIs (Google Drive, Dropbox metadata integration)
- [ ] Cloud API support (OneDrive/Google Drive)
- [ ] Add GitHub Actions for CI testing
- [ ] Add Dockerfile for containerized deployment (optional for servers)
- [ ] Consider whether --rebuild-folders option is necessary
- [ ] Rename Forced rescan to forced version (new version for every supported file)
- [ ] Add an option switch to the script to output all details for a specified file (parameter of the option)

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
