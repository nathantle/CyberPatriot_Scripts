import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def update_packages():
    print("Updating packages...")

    run_command("sudo apt update -y")
    run_command("sudo apt upgrade -y")
    run_command("sudo apt autoremove -y")

    print("Updated packages.")

def configure_firewall():
    print("Configuring firewall...")

    run_command("sudo ufw enable")
    run_command("sudo ufw allow ssh")
    run_command("sudo ufw status verbose")

    print("Firewall configured")

def disable_ssh_root_login():
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
    
def enforce_ssh_key_authentication():
    print("Enforcing SSH key authentication...")

    #Disable password authentication in SSH server configuration
    run_command("sudo sed -i s/#PasswordAuthentication yes/PasswordAuthentication no/ /etc/ssh/sshd.config")

    #Restart SSH service
    run_command("sudo systemctl restart ssh")

    print("SSH key based authentication has been enforced.")

def change_passwords(users, new_password):
    print("Changing passwords...")

    for user in users:
        #Change the password using passwd
        passwd_process = subprocess.Popen(['sudo', 'passwd', user], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        passwd_process.communicate(input=f'{new_password}\n{new_password}\n'.encode())

        # Check the exit code to determine if the password change was successful
        if passwd_process.returncode == 0:
            print(f"Password changed successfully for user '{user}'")
        else:
            print(f"Failed to change password for user '{user}'")

def remove_bad_services():
    print("Removing bad services...")

    #Removing telnet and ftp
    run_command("sudo apt remove -purge -y telnet ftp")

def set_log_file_permissions():
    print("Setting appropiate permissions on the log file")

    #Removing rwx for o and g
    run_command("sudo chmod -R g-rwx, o-rwx /var/log")

def lock_out_root():
    print("Locking out root user...")

    run_command("sudo passwd -l root")

    print("Root user locked out")

def disable_guest():
    print("Disabling guest account...")

    run_command()

# DO NOT FORGET TO SET THESE VARIBLES
# Configuring user_list and new_password for change password function
user_list = ['user1', 'user2', 'user3']
new_password = "new_password"

def main():
    # update_packages()
    #disable_ssh_root_login()
    # change_passwords(user_list, new_password)
    # enforce_ssh_key_authentication()
    remove_bad_services()
    set_log_file_permissions()
    lock_out_root()
    # disable_guest()
