import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def get_user_list():
    command = "cut -d: -f1 /etc/passwd"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        user_list = output.decode().splitlines()
        default_user = input("What is the default root user found in the README file on the desktop?").lower()
        user_list.remove(default_user)
        return user_list
    else:
        print(f"Error: {error.decode()}")
        return []

def basics(users, new_passsword):
    print("Updating packages...")

    run_command("sudo apt update -y")
    run_command("sudo apt upgrade -y")
    run_command("sudo apt autoremove -y")

    print("Updated packages.")
    print("Configuring firewall...")

    run_command("sudo ufw enable")
    run_command("sudo ufw allow ssh")
    run_command("sudo ufw status verbose")

    print("Firewall configured")
    print("Deleting unauthorized users")

    done = False

    admins = []

    while(done == False):
        admin = input("Enter authorized admin: ")
        finished = input("Are there any more?(y/n)").lower()

        admins.append(admin)

        if(finished == "y"):
            done = True
        elif(finished == "n"):
            done = False

    print("Changing user passwords...")

    for user in get_user_list():
        #Change the password using passwd
        if(user not in ["root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "systemd.network", "systemd-resolve", "messagebus", "systemd-timesync", "syslog", "_apt", "tss", "uuidd", "avahi-autoipd", "usbmux", "dnsmasq", "kernoops", "avahi", "cups-pk-helper", "rtkit", "whoopsie", "sssd", "speech-dispatcher", "nm-openvpn", "saned", "colord", "geoclue", "pulse", "gnome-initial-setup", "hplip", "gdm", "_rpc", "statd", "sshd", "systemd-network", "systemd-oom", "tcpdump"]):
            passwd_process = subprocess.Popen(['sudo', 'passwd', user], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            passwd_process.communicate(input=f'{new_password}\n{new_password}\n'.encode())

            # Check the exit code to determine if the password change was successful
            if passwd_process.returncode == 0:
                print(f"Password changed successfully for user '{user}'")
            else:
                print(f"Failed to change password for user '{user}'")

    print("Locking out root user...")

    run_command("sudo passwd -l root")

    print("Root user locked out")
    print("Removing bad services...")

    #Removing telnet and ftp
    run_command("sudo apt purge -y telnet ftp telnetd vsftpd")
    print("Bad services removed")

def ssh():

    run_command("sudo apt install ssh")

    print("Disabling SSH root login...")

    #Back up SSH config file
    run_command("sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")

    #Open SSH config file for editing
    with open("/etc/ssh/sshd_config", "r") as f:
        lines = f.readlines()

    #Update SSH configuration
    updated_lines = []
    for line in lines:
        if line.startswith("PermitRootLogin"):
            updated_lines.append("PermitRootLogin no/n")
        else:
            updated_lines.append(line)

    #Write updating configuration to file
    with open("/etc/ssh/sshd_config", "w") as f:
        f.writelines(updated_lines)

    #Restart SSH service
    run_command("sudo service ssh restart")

    print("SSH root login disabled.")

    print("Enforcing SSH key authentication...")

    #Disable password authentication in SSH server configuration
    run_command("sudo sed -i s/#PasswordAuthentication yes/PasswordAuthentication no/ /etc/ssh/sshd.config")

    #Restart SSH service
    run_command("sudo systemctl restart ssh")

    print("SSH key based authentication has been enforced.")

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

new_password = "Cyb3rP@triot24!"

def main():
    # update_packages()
    #disable_ssh_root_login()
    # enforce_ssh_key_authentication()'
    basics(get_user_list(), new_password)
    ssh()
    # set_log_file_permissions()
    # disable_guest()

    print("System secured.")

if __name__ == "__main__":
    main()
