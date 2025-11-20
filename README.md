# 🗄️ DBBackup — Universal Database Backup Utility

**DBBackup** is a powerful and extensible **command-line utility** written in **Python** for automating database backup and restoration across multiple database management systems (DBMS).  
It supports **full**, **incremental**, and **differential** backups, local and cloud storage, compression, and detailed logging — designed for both developers and system administrators managing mission-critical data.

---

## 🚀 Features

- **Multi-DBMS Support**
  - PostgreSQL
  - MySQL / MariaDB
  - MongoDB
  - SQLite
  - (Extensible for other databases)

- **Backup Types**
  - 🧱 **Full Backup** — complete copy of the entire database.
  - ⚙️ **Incremental Backup** — saves only changes made since the last backup.
  - 🔄 **Differential Backup** — saves changes made since the last full backup.

- **Storage Options**
  - Local directory storage
  - Cloud storage: **AWS S3**, **Google Cloud Storage**, **Azure Blob Storage**
  - Configurable backup retention policies

- **Backup Compression**
  - Optional compression using ZIP, Gzip, or Tar to minimize storage size.

- **Scheduling**
  - Automatic backup scheduling using **cron (Linux/macOS)** or **Windows Task Scheduler**.
  - Support for custom scheduling intervals.

- **Restore Operations**
  - Full or selective restore (specific tables/collections where supported)
  - Restore from local or cloud backups.

- **Logging & Notifications**
  - Detailed logs of each backup (start time, end time, duration, size, status)
  - Error and success logs
  - Optional **Slack notifications** for completion and error alerts

- **Cross-Platform**
  - Works on **Windows**, **macOS**, and **Linux**

---

## 🧰 Tech Stack

- **Language:** Python 3.10+
- **CLI Framework:** `typer`
- **Database Drivers:**
  - `psycopg[binary]` for PostgreSQL
  - `pymysql` for MySQL
  - `pymongo` for MongoDB
  - `sqlite3` (built-in)
- **Compression:** `gzip`, `zipfile`, or `tarfile`
- **Cloud SDKs:** `boto3`, `google-cloud-storage`, `azure-storage-blob`
- **Scheduler:** `APScheduler`
- **Logging:** `loguru`

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/LiveServers/dbbackup.git
cd dbbackup

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

#Using Docker - recommended

# 1. Make sure you create a config.json in the root dir matching this schema
class ConfigType(TypedDict):
    db_name: str
    db_host: str
    db_port: str
    db_username: str
    db_password: str
    db_type: str
    output_path: str

# If you want to upload to s3, extend the config with 
    bucket_name: str
    region: str
    access_key_id: str
    secret_access_key: str

# 2. Build your image
#Always pass either s3 or local for the storage_type inside Docker
docker build -t db-backup-tool .

# 3. Run your container - maps from app/backups to your localhost backups directory
# By default, files will be stored in local file directory
docker run --rm -it \
  -v $(pwd)/backups:/app/backups \
  db-backup-tool

#if using s3 storage, add the "--storage-type", "s3" to the Docker CMD

#if you want to see the logs, add "--verbose"

# 4. Test connection to your db
# 5. Connect to db, enter password, and create a data dump - results will resemble -> local_storage/laundromat-2025-10-23_13-08-49_backup.dump

