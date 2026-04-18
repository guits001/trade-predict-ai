import subprocess
import sys
import os

os.chdir(r"C:\Users\hp\OneDrive\Desktop\personalProject")

api_proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "5000"],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
)

import time
time.sleep(3)

dashboard_proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8501"],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
)

print("API running at http://localhost:5000")
print("Dashboard running at http://localhost:8501")
print("Press Ctrl+C to stop")

try:
    api_proc.wait()
except KeyboardInterrupt:
    api_proc.terminate()
    dashboard_proc.terminate()