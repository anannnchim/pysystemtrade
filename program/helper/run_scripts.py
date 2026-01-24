from pathlib import Path
import subprocess
import sys


# Resolve pysystemtrade root once
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_scripts(script_paths):
    """
    Run Python scripts relative to pysystemtrade root.

    script_paths: list[str | Path]
        e.g. "projects/01_running_system_f1/update_data_gg.py"
    """
    for script in script_paths:
        try:
            script_path = PROJECT_ROOT / script
            script_path = script_path.resolve()

            print(f"Running script: {script_path}")

            subprocess.run(
                [sys.executable, str(script_path)],
                check=True
            )

            print(f"Completed: {script_path}\n")

        except subprocess.CalledProcessError as e:
            print(f"Error while running script {script_path}: {e}")
            break

if __name__ == '__main__':
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    print(PROJECT_ROOT)
