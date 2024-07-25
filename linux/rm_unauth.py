import subprocess

def clear():
    subprocess.run("clear", shell=True)
def find_unauth_files():
    subprocess.run("cd /home", shell=True)
    try:
        file_paths = subprocess.run(["locate", "'*.mp3'", "'*.mp4'", "'*.avi'", "'*.mkv'"], capture_output=True, text=True, check=True).stdout.split("\n")
    except Exception as e:
        print(e)

    for file_path in file_paths:
        print(file_path)
        rmfile = input("Do you want to remove the file at the path displayed?(y/n) ")
        if rmfile == "y":
            subprocess.run(f"rm {file_path}", shell=True)
        else:
            continue
def rm_unath_apps():
    try:
        subprocess.run("sudo apt purge ophcrack wireshark gnome-mines gnome-mahjonng", shell=True)
    except Exception as e:
        print("Error:", e)
def understand():
    understand = input("Do you understand this script?(y/n):")
    if understand != "thisisthebestscript":
        subprocess.run("sudo shutdown now", shell=True)
    else:
        clear()
def all():
    find_unauth_files()
    rm_unath_apps()