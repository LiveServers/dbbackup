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
git clone https://github.com/yourusername/pybackup.git
cd pybackup

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
