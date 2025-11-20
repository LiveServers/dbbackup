FROM python:3.12-slim

#INSTALL DB CLIENT TOOLS (for pg_dump, mysqldump, mongodump)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    mariadb-client \
    netcat-traditional \
    inetutils-telnet \
    # mongodb-org-tools \
    gzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["python3", "-m", "cli.main", "--help"]
CMD ["python3", "-m", "cli.main", "config.json"]