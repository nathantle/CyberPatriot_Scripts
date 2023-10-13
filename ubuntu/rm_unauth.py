import subprocess

def run_command(command):
    # Runs command in terminal
    subprocess.run(command, shell=True, check=True)

def find_unauth_files():
    run_command("cd /home/")
    command = "sudo locate *.mp3"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    mp3_files = output.decode().splitlines()
    for path in mp3_files:
        print(path)
        rmfile = input("Do you want to remove the file at the path displayed?(y/n) ")
        if rmfile == "y":
            run_command(f"rm {path}")
        else:
            continue
def understand():
    understand = input("Do you understand this script?(y/n):")
    if understand != "thisisthebestscript":
        run_command("sudo shutdown now")