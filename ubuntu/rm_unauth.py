import subprocess

def run_command(command):
    # Runs command in terminal
    subprocess.run(command, shell=True, check=True)

def find_unauth_files():
    run_command("cd /home/")
    command = "sudo locate *.mp3"
    try:
        file_paths = subprocess.run(["locate", "*.mp3", "*.mp4", "*.avi", "*.mkv"], capture_output=True, text=True, check=True).stdout.split("\n")
    except Exception as e:
        print(e)

    for file_path in file_paths:
        print(file_paths)
        rmfile = input("Do you want to remove the file at the path displayed?(y/n) ")
        if rmfile == "y":
            run_command(f"rm {file_path}")
        else:
            continue
        
def understand():
    understand = input("Do you understand this script?(y/n):")
    if understand != "thisisthebestscript":
        run_command("sudo shutdown now")