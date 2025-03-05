
import os
import hashlib
import datetime
import json
import shutil
import sys
import smtplib
import argparse
from email.mime.text import MIMEText

parser = argparse.ArgumentParser(description="DocTrail - Document Versioning System")

parser.add_argument("annotation_root",   help="Root folder for annotations")
parser.add_argument("admin_folder",      help="Folder for logs and admin files")
parser.add_argument("alert_email",       help="Email address for error notifications")
parser.add_argument("--no-email",        help="Disable email notifications",               action="store_true")
parser.add_argument("--scan-file",       help="Scan a single file")
parser.add_argument("--rescan-all",      help="Force rescan of all files",                 action="store_true")
parser.add_argument("--rebuild-folders", help="Rebuild missing history folders",           action="store_true")

args = parser.parse_args()

ANNOTATION_ROOT = args.annotation_root
ADMIN_FOLDER = args.admin_folder
ALERT_EMAIL = args.alert_email

GLOBAL_LOG = os.path.join(ADMIN_FOLDER, "version_log.md")
os.makedirs(ADMIN_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".md", ".csv", ".png", ".jpg"}

def calculate_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def normalize_filename(filename):
    return filename.strip().replace(" ", "_").lower()

def get_hidden_folder_path(file_path):
    dirname, filename = os.path.split(file_path)
    basename, ext = os.path.splitext(filename)
    normalized = normalize_filename(f"{basename}_{ext[1:]}")
    return os.path.join(dirname, f".{normalized}")

def get_hash_file_path(hidden_folder):
    return os.path.join(hidden_folder, "hash.json")

def log_global(timestamp, event):
    with open(GLOBAL_LOG, "a") as log:
        log.write(f"[{timestamp}] {event}\n")

def send_alert(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "versioning-system@localhost"
        msg["To"] = ALERT_EMAIL
        with smtplib.SMTP("localhost") as server:
            server.sendmail(msg["From"], [ALERT_EMAIL], msg.as_string())
    except Exception as e:
        print(f"Failed to send alert email: {e}")

def conditional_alert(subject, body):
    if not args.no_email:
        send_alert(subject, body)

def process_file(file_path, force_rescan=False):
    if os.path.splitext(file_path)[1].lower() not in ALLOWED_EXTENSIONS:
        return

    if os.path.splitext(file_path)[1] == "":
        log_global(datetime.datetime.now().isoformat(), f"[ERROR] File without extension: {file_path}")
        conditional_alert("Versioning Error - No Extension", f"File {file_path} has no extension and was ignored.")
        return

    hidden_folder = get_hidden_folder_path(file_path)
    hash_file = get_hash_file_path(hidden_folder)

    if not os.path.exists(hidden_folder):
        os.makedirs(hidden_folder)
        log_global(datetime.datetime.now().isoformat(), f"[NEW] Created history folder for: {file_path}")

    if not os.path.exists(hash_file):
        with open(hash_file, 'w') as f:
            json.dump({"hash": None}, f)
        log_global(datetime.datetime.now().isoformat(), f"[NEW] Created hash file for: {file_path}")

    current_hash = calculate_file_hash(file_path)

    previous_hash = None
    with open(hash_file, 'r') as f:
        data = json.load(f)
        previous_hash = data.get("hash")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%f")

    if previous_hash is None:
        log_global(timestamp, f"[ENROLL] First-time enrollment: {file_path}")

    if force_rescan or current_hash != previous_hash:
        dirname, filename = os.path.split(file_path)
        basename, ext = os.path.splitext(filename)
        normalized_basename = normalize_filename(basename)
        versioned_filename = f"{normalized_basename}_{timestamp}{ext}"
        versioned_path = os.path.join(hidden_folder, versioned_filename)
        shutil.copy2(file_path, versioned_path)
        log_global(timestamp, f"[VERSION] {filename} saved as {versioned_filename}")
        with open(hash_file, 'w') as f:
            json.dump({"hash": current_hash}, f)

def full_scan(force_rescan=False):
    for root, dirs, files in os.walk(ANNOTATION_ROOT):
        # filter out dot folders
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for file in files:
            # filter out dot files
            if file.startswith("."):
                continue
            process_file(os.path.join(root, file), force_rescan)

if args.scan_file:
    process_file(args.scan_file, force_rescan=args.rescan_all)
elif args.rebuild_folders:
    full_scan(force_rescan=args.rescan_all)
else:
    full_scan(force_rescan=args.rescan_all)
