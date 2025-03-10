import subprocess

def run_scripts(scripts):
    """
    Run a list of Python scripts sequentially.
    :param scripts: List of script file paths to execute.
    """
    for script in scripts:
        try:
            print(f"Running script: {script}")
            subprocess.run(["python3", script], check=True)
            print(f"Completed: {script}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error while running script {script}: {e}")
            break
