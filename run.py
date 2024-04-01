import os 
import psutil
from pathlib import Path

process_names = [proc.name() for proc in psutil.process_iter()]
    
if Path(f"{Path.cwd()}/temp_files/input").exists() and Path(f"{Path.cwd()}/temp_files/output").exists():
     pass
else:
     Path(f"{Path.cwd()}/temp_files/input").mkdir(parents=True)
     Path(f"{Path.cwd()}/temp_files/output").mkdir(parents=True)

os.system(f"{Path.cwd()}/app.py")
