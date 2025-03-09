import datetime
import json
import hashlib
import os
import shutil
import sys
import argparse
import smtplib
from email.mime.text import MIMEText

###########################################################
# Argument Parsing
#
parser = argparse.ArgumentParser(description="DocTrail - Document Versioning System")

parser.add_argument("projects_folder", help="Folder where active documents are stored")
parser.add_argument("history_folder", help="Folder where version history is stored")
parser.add_argument("admin_folder", help="Folder for logs and admin files")
parser.add_argument("alert_email", help="Email address for error notifications")

# Scan modes
parser.add_argument("--consistency-scan", action="store_true", help="Hybrid scan (timestamp + hash if needed) (default)")
parser.add_argument("--hash-scan", action="store_true", help="Always use full hash scan")
parser.add_argument("--mtime-scan", action="store_true", help="Fast scan using only timestamps")
parser.add_argument("--scan-file", help="Scan a specific file only")
parser.add_argument("--force-version", action="store_true", help="Force rescan of all files")

# Additional options
parser.add_argument("--no-email",        help="Disable email notifications",               action="store_true")

args = parser.parse_args()

# Ensure only one scan mode is selected
conflict_sum = sum([args.consistency_scan, args.hash_scan, args.mtime_scan])
if conflict_sum > 1:
    print("❌ Conflicting scan modes! Use only one: --hash-scan, --consistency-scan, or --mtime-scan.")
    sys.exit(1)

# Set default scan mode if none is selected
if conflict_sum == 0:
    args.mtime_scan = True  # default

# Define global variables
PROJECTS_ROOT = args.projects_folder
HISTORY_ROOT = args.history_folder
ADMIN_FOLDER = args.admin_folder
ALERT_EMAIL = args.alert_email


GLOBAL_LOG = os.path.join(ADMIN_FOLDER, "version_log.md")
os.makedirs(ADMIN_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".md", ".csv", ".png", ".jpg"}

# Initialize statistics dictionary
statistics = {
    "total_files": 0,
    "checked_files": 0,
    "orphan_files": 0,
    "new_versions": 0,
    "touched_but_unchaged_files": 0,
    "inconsistent_files": 0,               # --consistency-scan only
    "errors": 0
    }



###########################################################
# Helper functions
#
def get_timestamp(time=0):
    time = datetime.datetime.now() if time == 0 else time
    return time.strftime("%Y-%m-%dT%H-%M-%S-%f")

def calculate_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def normalize_filename(filename):
    return filename.strip().replace(" ", "_").lower()

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

def get_history_folder_for_file(file_path):
    relative_path = os.path.relpath(file_path, PROJECTS_ROOT)
    folder, filename = os.path.split(relative_path)
    basename, ext = os.path.splitext(filename)
    normalized = normalize_filename(f".{basename}_{ext[1:]}")

    project_history_folder = os.path.join(HISTORY_ROOT, f".{folder}")
    os.makedirs(project_history_folder, exist_ok=True)

    return os.path.join(project_history_folder, normalized)


def create_new_version(file_path, history_folder, timestamp):
    dirname, filename = os.path.split(file_path)
    basename, ext = os.path.splitext(filename)
    normalized_basename = normalize_filename(basename)
    versioned_filename = f"{normalized_basename}_{timestamp}{ext}"
    versioned_path = os.path.join(history_folder, versioned_filename)
    shutil.copy2(file_path, versioned_path)
    log_global(timestamp, f"[VERSION] {file_path} saved as {versioned_filename}")


def update_hash_file(file, hash=None, mtime=0, timestamp=0):
    data = {    "last_version_hash": hash,
                "last_version_mtime": mtime,
                "last_version_timestamp": timestamp }
    with open(file, 'w') as f:
        json.dump(data, f)
    log_global(timestamp, f"[HASH] {file} updated")

def read_hash_file(hash_file_path):
    data = {}
    with open(hash_file_path, 'r') as f:
        data = json.load(f)
    return (
        data.get("last_version_hash"),
        data.get("last_version_mtime"),
        data.get("last_version_timestamp")
    )        

###########################################################
# Main function
#
def process_file(current_file_path, force_version=False):
    statistics["total_files"] += 1
    if os.path.splitext(current_file_path)[1].lower() not in ALLOWED_EXTENSIONS:
        return

    statistics["checked_files"] += 1
    history_folder = get_history_folder_for_file(current_file_path)
    hash_file_path = get_hash_file_path(history_folder)

    if not os.path.exists(history_folder):
        os.makedirs(history_folder)
        statistics["orphan_files"] += 1

    if not os.path.exists(hash_file_path):
        update_hash_file(hash_file_path)

    last_version_hash, last_version_mtime, _ = read_hash_file(hash_file_path)

    current_mtime = os.path.getmtime(current_file_path)
    timestamp = get_timestamp()

    if force_version:
        current_hash = calculate_file_hash(current_file_path)
        create_new_version(current_file_path, history_folder, timestamp)
        update_hash_file(hash_file_path, current_hash, current_mtime, timestamp)
        statistics["new_versions"] += 1

    elif args.hash_scan:
        # the most secure way to detect changes
        current_hash = calculate_file_hash(current_file_path)
        if current_hash != last_version_hash:
            create_new_version(current_file_path, history_folder, timestamp)
            update_hash_file(hash_file_path, current_hash, current_mtime, timestamp)
            statistics["new_versions"] += 1

    elif args.mtime_scan:
        # no need to calculate hash if no change in mtime
        if current_mtime > last_version_mtime:
            current_hash = calculate_file_hash(current_file_path)
            if current_hash != last_version_hash:
                create_new_version(current_file_path, history_folder, timestamp)
                update_hash_file(hash_file_path, current_hash, current_mtime, timestamp)
                statistics["new_versions"] += 1
            else:  # touched but unchanged
                update_hash_file(hash_file_path, current_hash, current_mtime, timestamp)
                statistics["touched_but_unchaged_files"] += 1

    elif args.consistency_scan:
        # consistency check
        current_hash = calculate_file_hash(current_file_path)
        #print(f'----- {current_file_path} --------------')
        #print(current_mtime, last_version_mtime)
        #print(current_hash, last_version_hash)
        if  not ( current_mtime >= last_version_mtime and current_hash == last_version_hash ):
            log_global(timestamp, f"[INCONSISTENCY] {current_file_path} has inconsistent hash and mtime")         
            statistics["inconsistent_files"] += 1

    else:
        pass    


def full_scan(force_version=False):
    for root, dirs, files in os.walk(PROJECTS_ROOT):
        # filter out dot folders
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for file in files:
            # filter out dot files
            if file.startswith("."):
                continue
            print('.')
            process_file(os.path.join(root, file), force_version)



############################################
# Main
############################################


############################################
# Start
#
start_time = datetime.datetime.now()
log_global(get_timestamp(start_time), "[START] Versioning script started" + '\n' + json.dumps(vars(args), indent=4))

if args.scan_file:
    process_file(args.scan_file, force_version=args.force_version)
else:
    full_scan(force_version=args.force_version)

############################################
# End of the script
#
end_time = datetime.datetime.now()
log_global(get_timestamp(end_time), "[END] Versioning script ended" + '\n' + json.dumps(statistics, indent=4))

# Calculate and log the total running time
total_time = end_time - start_time
log_global(get_timestamp(end_time), f"[INFO] Total running time: {total_time}")
