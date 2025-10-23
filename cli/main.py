import typer
from utils.load_config import load_config
from utils.precheck import check_binaries, test_connection
from core.manager import BackupManager

app = typer.Typer()

@app.command()
def backup(config: str):
    config = load_config(config)
    check_binaries(config["db_type"])
    test_connection(config)
    manager = BackupManager(config=config)
    result = manager.run_postgres_backup()
    typer.echo(f"Backup stored at: {result}")

if __name__ == "__main__":
    app()