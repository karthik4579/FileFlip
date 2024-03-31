import os 
import psutil
from pathlib import Path

process_names = [proc.name() for proc in psutil.process_iter()]


# Check if process name matches unoserver
if 'unoserver' in process_names:
      pass
else:
    os.system('unoserver >> /dev/null &')
    
if Path(f"{Path.cwd()}/temp_files/input").exists() and Path(f"{Path.cwd()}/temp_files/output").exists():
     pass
else:
     Path(f"{Path.cwd()}/temp_files/input").mkdir(parents=True)
     Path(f"{Path.cwd()}/temp_files/output").mkdir(parents=True)

os.system(f"{Path.cwd()}/env/bin/python {Path.cwd()}/app.py")