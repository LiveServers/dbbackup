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
  - Daily backups inside Docker using **APScheduler** (default: **9:00pm Africa/Nairobi**).
  - Custom time (`--at HH:MM`) and timezone (`--timezone` / `TZ`).

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

# 2. Run with Docker Compose (recommended)
# Builds the image, keeps the container running, and restarts it after reboot.
# Dumps land in ./backups on the host. Default schedule: 21:00 Africa/Nairobi.
docker compose up -d --build

# Watch startup logs — you should see the next scheduled run:
docker compose logs -f dbbackup

# Stop the scheduler:
docker compose down

# 3. One-off backup (no schedule) — container exits when the dump finishes
docker build -t db-backup-tool .
docker run --rm -it \
  -v $(pwd)/config.json:/app/config.json:ro \
  -v $(pwd)/backups:/app/backups \
  db-backup-tool \
  python3 -m cli.main config.json --verbose

# Scheduled backup without Compose (container must stay running — do not use --rm)
docker run -d --restart unless-stopped --name dbbackup \
  -e TZ=Africa/Nairobi \
  -v $(pwd)/config.json:/app/config.json:ro \
  -v $(pwd)/backups:/app/backups \
  db-backup-tool

# S3: add --storage-type s3 to the command (and include S3 keys in config.json)

# Dump filenames look like:
# backups/laundromat-2025-10-23_13-08-49_backup.dump
```

## Daily schedule

By default the image runs:

```bash
python3 -m cli.main config.json --verbose --schedule --at 21:00
```

| Flag | Default | Meaning |
| --- | --- | --- |
| `--schedule` | off (on in Docker `CMD`) | Keep the process alive and backup every day |
| `--at` | `21:00` | Daily time in 24-hour `HH:MM` |
| `--timezone` | `TZ` env, else `Africa/Nairobi` | IANA timezone for `--at` |
| `--verbose` | off (on in Docker `CMD`) | Log `pg_dump` output |
| `--storage-type` | `local` | `local` or `s3` |

Change timezone in `docker-compose.yml`:

```yaml
environment:
  TZ: Africa/Nairobi
```

Change the clock time by editing the `CMD` in the `Dockerfile`, or override it:

```bash
docker compose run --rm dbbackup python3 -m cli.main config.json --verbose --schedule --at 21:00 --timezone Africa/Nairobi
```

