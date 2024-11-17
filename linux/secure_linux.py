'''
CyberPatriot Linux Script
Written by Nathan Le

Designed to fix security issues and earn points in the CyberPatriot Competition
'''
import subprocess
import util
END_MSG = '''
Security Issues not automated yet:
- System updates checked daily
- Removing unauthorized software and files
- SSH Root login disabled
- Password and account policies
'''
# Tuple of default users that should not have changes made to
DEFAULT_USERS = ("lightdm", "systemd-coredump", "root", "daemon", "bin", "sys", "sync", "games", "man", "lp", 
                 "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "systemd.network", 
                 "systemd-resolve", "messagebus", "systemd-timesync", "syslog", "_apt", "tss", "uuidd", "avahi-autoipd", 
                 "usbmux", "dnsmasq", "kernoops", "avahi", "cups-pk-helper", "rtkit", "whoopsie", "sssd", "speech-dispatcher", 
                 "nm-openvpn", "saned", "colord", "geoclue", "pulse", "gnome-initial-setup", "hplip", "gdm", "_rpc", "statd", 
                 "sshd", "systemd-network", "systemd-oom", "tcpdump", "_flatpak", "fwupd-refresh", "dovecot", "dovenull", "ntp", "ftp")
# Tuple of common bad services
BAD_SERVICES = ("nginx")

# Tuple of common bad apps
BAD_APPS = ("nginx", "remmina-common", "aisleriot", "wireshark", "ophcrack", "ettercap-common", "ettercap-graphical", 
            "ettercap-text-only", "deluge-gtk", "deluge", "gnome-mines", "gnome-mahjonng")

# Tuple of possible package managers
PACKAGE_MANAGERS = ("apt", "yum", "apt-get")

# String that stores the user account that should not have changes made to
YOU = input("Enter your username: ").lower()

SSH_CRIT_SERV = input("Is ssh a critical service? (y/n) ").lower()
FTP_CRIT_SERV = input("Is FTP a critical service? (y/n)" ).lower()

if FTP_CRIT_SERV == "n":
    subprocess.run("sudo purge vsftpd", shell=True)
    subprocess.run("sudo systemctl stop vsftpd", shell=True)
    subprocess.run("sudo systemctl disable vsftpd", shell=True)

# Declare lists to store current users, authorized admins and users
current_users = []
auth_admins = []
auth_users = []
# Final string that stores a secure password
SECURE_PASSWORD = "Cyb3rP@triot25!" 

# Handle updates
proceed = input("Press enter to proceed to updates(s to skip)")
if proceed != "s": 
    try:
        package_manager = input("Enter the package manager used on this system: ").lower()
        if package_manager not in PACKAGE_MANAGERS:
            print("You did not enter a valid package manager, restart the script")
        else:
            # Updates packages
            subprocess.run(f"sudo {package_manager} upgrade -y", shell=True)
            # Removes any leftover/unneccesary packages
            subprocess.run(f"sudo {package_manager} autoremove -y", shell=True)
    except Exception as e:
        print("Error updating packages")
        print(e)

# Configure Firewall
proceed = input("Press enter to proceed to configuring firewall(s to skip)")
if proceed != "s": 
    try:
        # Enables UFW
        subprocess.run("sudo ufw enable", shell=True)

        if SSH_CRIT_SERV == "y":
            # Allow SSH traffic
            subprocess.run("sudo ufw allow ssh", shell=True)
    except Exception as e:
        print("Error configuring firewall")
        print(e)

# Configure ssh
proceed = input("Press enter to proceed to configuring ssh(s to skip)")
if proceed != "s": 
    try:
        # Install/update ssh
        subprocess.run("sudo apt purge ssh", shell=True)
        subprocess.run("sudo apt purge openssh-server", shell=True)
        subprocess.run("sudo apt install ssh", shell=True)
        subprocess.run("sudo apt install openssh-server", shell=True)

        # Start/enable ssh service
        subprocess.run("sudo systemctl enable ssh", shell=True)
        subprocess.run("sudo systemctl start ssh", shell=True)

        # Disable SSH root login
        subprocess.run("sudo sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config", shell=True)

        # Restart SSH
        subprocess.run("sudo systemctl restart ssh", shell=True)
    except Exception as e:
        print(f"Error configuring ssh\n{e}")

proceed = input("Press enter to proceed to configuring security settings(s to skip)")
if proceed != "s":
    # Configure security settings
    try:
        # Update pam modules
        subprocess.run("sudo pam-auth-update", shell=True)

        # Install libpam-pwquality
        subprocess.run("sudo apt install libpam-pwquality", shell=True)

        # Sets account policy
        subprocess.run("sudo cp account_policy_files/faillock /usr/share/pam-configs/faillock", shell=True)
        subprocess.run("sudo cp account_policy_files/faillock_notify /usr/share/pam-configs/faillock_notify", shell=True)

        # Updates pam modules
        subprocess.run("sudo pam-auth-update", shell=True)

        # Password max age = 90
        subprocess.run("sudo sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS\t90/' /etc/login.defs", shell=True)

        # Password min age = 15
        subprocess.run("sudo sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS\t15/' /etc/login.defs", shell=True)

        # Null passwords do not authenticate
        subprocess.run("sudo sed -i s/nullok//g /etc/pam.d/common-auth", shell=True)

        # Minimum password length = 10
        subprocess.run("sudo sed -i '/pam_pwquality.so/ s/$/ minlen=10/' /etc/pam.d/common-password", shell=True)

        # IPv4 forwarding has been disabled
        subprocess.run("sudo sed -i 's/net.ipv4.ip_forward.*/net.ipv4.ip_forward=0/' /etc/sysctl.conf", shell=True)

        # IPv4 TCP SYN cookies has been enabled
        subprocess.run("sudo sed -i 's/net.ipv4.tcp_syncookies.*/net.ipv4.tcp_syncookies=1/' /etc/sysctl.conf", shell=True)

        # Address space layout randomization has been enabled
        subprocess.run("sudo sed -i 's/.*kernel.randomize_va_space.*/kernel.randomize_va_space=2/g' /etc/sysctl.conf", shell=True) # Addresss space layout randomization enabled

        # Sudo requires authentication
        subprocess.run("sudo sed -i 's/!authenticate/authenticate/' /etc/sudoers", shell=True)

        # Refreshes changes made to /etc/sysctl.conf
        subprocess.run("sudo sysctl --system", shell=True)

        # Refreshes changes made to pam
        subprocess.run("sudo pam-auth-update", shell=True)

        # Sets secure permissions on shadow file
        subprocess.run("sudo chmod -R 640 /etc/shadow", shell=True) 

        # Locks root account
        subprocess.run("sudo passwd -l root", shell=True)
    except Exception as e:
        print(e)

# Handle Users
proceed = input("Press enter to proceed to handle users(s to skip)")
if proceed != "s": 
    try:
        # List of current users on machine
        process = subprocess.run("getent passwd | cut -d: -f1", 
                                   shell=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   text=True)
        current_users = process.stdout.splitlines()

        # Subtracts system and default users
        current_users = list(set(current_users) - set(DEFAULT_USERS) - {YOU})
    except Exception as e:
        print(e)

    subprocess.run("clear", shell=True)
    input("Create a new terminal and enter the authorized administrators into the auth_admins.txt file, seperated by newlines, press enter when done")

    process = subprocess.run("sudo cat auth_admins.txt", 
                             shell=True, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             text=True)
    # Fill list of authorized administrators
    auth_admins = process.stdout.splitlines()

    process = subprocess.run("sudo cat auth_users.txt", 
                             shell=True, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             text=True)
    # Fill list of authorized users
    auth_users = process.stdout.splitlines()

    subprocess.run("clear", shell=True)
    input("Create a new terminal and enter the authorized users(not admins) into the auth_users.txt file, seperated by newlines, press enter when done")

    for current_user in current_users:
        # If current_user is not authorized administrator or user
        if current_user not in auth_admins and current_user not in auth_users:
            try:
                print(f"Deleting user {current_user}")
                subprocess.run(f"sudo userdel {current_user}", shell=True)
                current_users.remove(current_user)
            except:
                print("Error deleting user")

    for current_user in current_users:
        admin = util.is_user_admin(current_user)
        if admin and current_user not in auth_admins:
            try:
                # Make user not administrator
                print(f"Removing {current_user} from group sudo")
                subprocess.run(f"sudo gpasswd -d {current_user} sudo", shell=True)
            except:
                print("Error deleting user from group sudo")
        elif not admin and current_user in auth_admins:
            try:
                # Make user administrator
                print(f"Adding {current_user} to group sudo")
                subprocess.run(f"sudo gpasswd -a {current_user} sudo", shell=True)
            except:
                print("Error adding user to group sudo")

        # Sets password for every user except default user
        process = subprocess.Popen(f"sudo passwd {current_user}", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate(input=f"{SECURE_PASSWORD}\n{SECURE_PASSWORD}\n")

try:
    process = subprocess.run("sudo locate -name '*.mp3' /home", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    file_paths = process.stdout.splitlines()

    for file_path in file_paths:
        delete = input(f"Do you want to delete the file @  {file_path}? (y/n)").lower()
        if delete == "y":
            subprocess.run(f"sudo rm {file_path}", shell=True)
except Exception as e:
    print(e)

# Delete the list of unauthorized apps
command = f"sudo apt purge "
for app in BAD_APPS:
    command += f"{app} "
subprocess.run(command, shell=True)    

command = f"sudo systemctl disable "
for bad_service in BAD_SERVICES:
    command += f"{bad_service} "
subprocess.run(command, shell=True)

print(END_MSG)
