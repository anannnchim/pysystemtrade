import subprocess

import subprocess
import sys

def run_scripts(scripts):
    for script in scripts:
        try:
            print(f"Running script: {script}")
            subprocess.run([sys.executable, script], check=True)
            print(f"Completed: {script}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error while running script {script}: {e}")
            break
