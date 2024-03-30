import psutil
import os


for proc in psutil.process_iter(['pid', 'name']):
        # Check if process name matches unoserver
        if proc.info['name'] == 'unoserver':
            pass
        else:
          os.system('unoserver >> /dev/null &')