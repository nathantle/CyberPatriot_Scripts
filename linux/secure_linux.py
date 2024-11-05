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
BAD_SERVICES = ("nginx", "apache2")

# Tuple of common bad apps
BAD_APPS = ("aisleriot", "wireshark", "ophcrack", "ettercap-common", "ettercap-graphical", "ettercap-text-only", "deluge-gtk", "deluge", "gnome-mines", "gnome-mahjonng")

# Tuple of possible package managers
PACKAGE_MANAGERS = ("apt", "yum", "apt-get")

# String that stores the user account that should not have changes made to
YOU = input("Enter your username: ").lower()

# Declare lists to store current users, authorized admins and users
current_users = []
auth_admins = []
auth_users = []
# Final string that stores a secure password
SECURE_PASSWORD = "Cyb3rP@triot25!" 

proceed = input("Press enter to proceed to updates(s to skip)")
if proceed != "s": 
    try:
        # Updates packages
        process = subprocess.run("sudo apt upgrade -y")
        # Removes any leftover/unneccesary packages
        process = subprocess.run("sudo apt autoremove -y")
    except Exception:
        print("Error updating packages")

# Configure Firewall
proceed = input("Press enter to proceed to configuring firewall(s to skip)")
if proceed != "s": 
    try:
        # Enables UFW
        process = subprocess.Popen(["sudo", "ufw", "enable"])
        process.wait()

        ssh_crit_serv = input("Is SSH a critical service (y/n)")
        if ssh_crit_serv.lower() == "y":
            # Allows SSH traffic
            process = subprocess.Popen(["sudo", "ufw", "allow", "ssh"])
            process.wait()
    except Exception:
        print("Error configuring firewall")

# Configure ssh
proceed = input("Press enter to proceed to configuring ssh(s to skip)")
if proceed != "s": 
    try:
        # Install/update and start ssh service
        process = subprocess.Popen(["sudo", "apt", "install","ssh"])
        process.wait()
        process = subprocess.Popen(["sudo", "systemctl", "enable","ssh"])
        process.wait()
        process = subprocess.Popen(["sudo", "systemctl", "start","ssh"])
        process.wait()

        # Disable SSH root login
        process = subprocess.Popen(["sudo", "sed", "-i", "'s/PermitRootLogin yes/PermitRootLogin no/g'", "/etc/ssh/sshd_config"])
        process.wait()

        # Restart SSH
        process = subprocess.Popen(["sudo", "systemctl", "restart", "ssh"])
        process.wait()
    except Exception:
        print("Error configuring ssh")

# Handle Users
proceed = input("Press enter to proceed to handle users(q to stop)")
if proceed != "q": 
    try:
        # List of current users on machine
        process = subprocess.Popen("getent passwd | cut -d: -f1", shell=True, stdout=subprocess.PIPE)
        output, error = process.communicate()
        current_users = output.decode("utf-8").splitlines()

        # Fills array of current users on the machine
        current_users = list(set(current_users) - set(DEFAULT_USERS) - {YOU})
    except Exception as e:
        print(e)

    # Fills list of authorized Admins
    while True:
        auth_admin = input("Enter authorized administrator(exclude yourself, type \"d\" when done, \"r\" to remove last entry): ")
        if auth_admin == "d":
            break
        elif auth_admin == "r" and auth_admins:
            # Removes last entry
            auth_admins.pop()
        else:
            # Adds user to list
            auth_admins.append(auth_admin)

    # Fills list of authorized users
    while True:
        auth_user = input("Enter authorized user(type \"d\" when done, \"r\" to remove last entry): ")
        if auth_user == "d":
            break
        elif auth_user == "r" and auth_users:
            # Removes last entry
            auth_users.pop()
        else:
            # Adds user to list
            auth_users.append(auth_user)

    for current_user in current_users:
        # If current_user is not authorized administrator or user
        if current_user not in auth_admins and current_user not in auth_users:
            try:
                print("Deleting user " + current_user)
                # Deleting user
                process = subprocess.Popen(["sudo", "userdel", current_user])
                process.wait()
                current_users.remove(current_user)
            except:
                print("Error deleting user")

    for user in current_users:
        admin = util.is_user_admin(user)
        if admin and user not in auth_admins:
            try:
                # Make user not administrator
                process = subprocess.Popen(["sudo", "gpasswd", "-d", user, "sudo"])
                process.wait()
            except:
                print("Error deleting user from group sudo")
        elif not admin and user in auth_admins:
            try:
                # Make user administrator
                process = subprocess.Popen(["sudo", "gpasswd", "-a", user, "sudo"])
                process.wait()
            except:
                print("Error adding user to group sudo")

        # Sets password for every user except default user
        process = subprocess.Popen(["sudo", "passwd", user], stdin=subprocess.PIPE)
        process.communicate(f"{SECURE_PASSWORD}\n{SECURE_PASSWORD}\n".encode())
        process.wait()

# Configure misc security settings
try:
    process = subprocess.Popen(["sudo", "pam-auth-update"]) # Updates pam modules
    process.wait()
    
    # Maybe locks root account sudo?
    # process = subprocess.Popen(["sudo", "passwd", "-l" "root"]) # Root password is no longer blank
    # process.wait()

    # "sudo sed -i 's/^PASS\_MAX\_DAYS.*/PASS_MAX_DAYS\t90/' /etc/login.defs"

    process = subprocess.Popen(["sudo", "sed", "-i", "/nullok/d", "/etc/pam.d/common-auth"]) # Null passwords do not authenticate
    process.wait()
    process = subprocess.Popen(["sudo", "sed", "-i", "s/.*kernel.randomize_va_space.*/kernel.randomize_va_space=2/g", "/etc/sysctl.conf"]) # Addresss space layout randomization enabled
    process.wait()
    process = subprocess.Popen(["sudo", "echo", "1", ">", "/proc/sys/net/ipv4/tcp_syncookies"]) # IPv4 TCP SYN cookies have been enabled
    process.wait()
    process = subprocess.Popen(["sudo", "sed", "-i", "s/.*net.ipv4.tcp_syncookies./net.ipv4.tcp_syncookies=1*", "/etc/sysctl.d/10-network-security.conf"]) # IPv4 TCP SYN cookies have been enabled at boot
    process.wait()
    # process = subprocess.Popen(["sudo", "sed", "-i"] )

    process = subprocess.Popen(["sudo", "sysctl", "--system"]) # Refreshes the changes above
    process.wait()

    process = subprocess.Popen(["sudo", "chmod", "-R", "640", "/etc/shadow" ]) # Sets secure permissions on shadow file
    process.wait()

except Exception as e:
    print(e)

# Error somehow occurs here
'''
# Look for unauthorized media files
try:
    process = subprocess.Popen(["sudo", "locate", "*.mp3"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()
    file_paths = output.splitlines()

    for file_path in file_paths:
        delete = input("Do you want to delete the file @ " + file_path + "(y/n) ").lower()
        if delete == "y":
            process = subprocess.Popen(["sudo", "rm", file_path])
            process.wait()
except Exception as e:
    print(e)
    print("Error occured while searching for media files")

# Try to delete the list of unauthorized apps
for app in BAD_APPS:
    process = subprocess.Popen(["sudo", "apt", "purge", app])
    process.wait()
process = subprocess.Popen(["sudo", "apt", "autoremove"])    

'''
print(END_MSG)
