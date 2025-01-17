import subprocess
'''
This one will update database for Diversified program.
'''

def run_scripts(scripts):
    """
    Run a list of Python scripts sequentially.
    :param scripts: List of script file paths to execute.
    """
    for script in scripts:
        try:
            print(f"Running script: {script}")
            subprocess.run(["python", script], check=True)
            print(f"Completed: {script}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error while running script {script}: {e}")
            break


if __name__ == '__main__':

    # Update futures related data
    scripts = [
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/startup.py",
    ]

    # Run the scripts
    run_scripts(scripts)
