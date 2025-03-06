
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
Projects/                    # Your active working files
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
```sh
git clone https://github.com/your-username/doctrail.git
cd doctrail
python3 -m venv venv
source venv/bin/activate
```

---

## ▶️ Usage Examples

### Full Scan (all files - default hybrid scan)
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com
```

### Explicit Scan Modes
```sh
# Full hash scan (slowest but most precise)
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --hash-scan --no-email

# Timestamp-only scan (fastest, lower precision)
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --timestamp-scan
```

### Single File Scan
```sh
python3 versioning_script.py ./Projects ./TrackedHistory ./Admin your@email.com --scan-file "./Projects/Project_A/Document_1.pdf"
```

---

## ✅ Supported File Types
- PDF, DOCX, TXT, XLSX, PPTX, MD, CSV, PNG, JPG

---

## 📧 Email Alerts
DocTrail can send email alerts if issues occur. Default uses local SMTP (Postfix).

---

## 📊 Future Ideas
- Cloud API support (OneDrive/Google Drive)
- GitHub Actions for testing
- Optional Dockerfile

---

## 📝 License
MIT License xxxxxxx

---

