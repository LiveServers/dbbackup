#shutil can comporess and create a zip file 
import os
import shutil

class LocalStorage:
    def save_backup(self, source_dir: str, destination_dir: str) -> str:
        os.makedirs(destination_dir, exist_ok=True)
        shutil.copy(source_dir, destination_dir)
        return os.path.join(destination_dir, os.path.basename(source_dir))