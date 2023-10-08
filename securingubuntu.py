import subprocess
import ubBasics

def run_command(command):
    subprocess.run(command, shell=True, check=True)
def set_log_file_permissions():
    print("Setting appropiate permissions on the log file")

    #Removing rwx for o and g
    run_command("sudo chmod -R g-rwx, o-rwx /var/log")

def disable_guest():
    print("""
    You will need to disable guest session manually. "" means to do the command
    "sudo systemctl status display-manager"
    If the main PID is gdm, remove gdm3 and install lightdm
    If lightdm, continue.
    "cd /usr/share/lightdm/lightdm.conf.d"
    "ls -la"
    If there is a no guest file, 
    "sudo gedit [filename]"
    add allow-guest=true
    """)

def main():
    ubBasics.all()

    print("System secured.")

if __name__ == "__main__":
    main()