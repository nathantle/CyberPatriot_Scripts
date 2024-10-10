import subprocess
import util
'''
CyberPatriot Ubuntu Script
Written by Nathan Le

Designed to fix security issues and earn points in the CyberPatriot Competition
'''

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
                 "sshd", "systemd-network", "systemd-oom", "tcpdump")

BAD_SERVICES = ("nginx")
BAD_APPS = ("aisleroot", "wireshark", "ophcrack", "")

# String that stores the user account that should not have changes made to
YOU = input("Enter your username: ").lower()

# Declare lists to store current users, authorized admins and users
current_users = []
auth_admins = []
auth_users = []

SECURE_PASSWORD = "Cyb3rP@triot25!"

# Manual Tasks - Configure Software and Updates
print("")

proceed = input("Press enter to proceed to updates(q to stop)")
if proceed != "q": 
    # Updates
    try:
        process = subprocess.Popen(["sudo", "apt", "update"])
        process.wait()
        process = subprocess.Popen(["sudo", "apt", "upgrade"])
        process.wait()
        process = subprocess.Popen(["sudo", "apt", "autoremove"])
        process.wait()
    except Exception:
        print("Error updating packages")

# Configure Firewall
proceed = input("Press enter to proceed to configuring firewall(q to stop)")
if proceed != "q": 
    try:
        process = subprocess.Popen(["sudo", "ufw", "enable"])
        process.wait()
    except Exception:
        print("Error configuring firewall")

# Configure ssh
proceed = input("Press enter to proceed to configuring ssh(q to stop)")
if proceed != "q": 
    try:
        # Update and start ssh service
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
        process = subprocess.Popen("getent passwd | cut -d: -f1", shell=True, stdout=subprocess.PIPE)
        output, error = process.communicate()
        current_users = output.decode("utf-8").splitlines()
        # Fills array of current users on the machine
        current_users = list(set(current_users) - set(DEFAULT_USERS) - {YOU})
    except Exception as e:
        print(e)
        print("Error handling users")

    # Fills list of authorized Admins
    while True:
        auth_admin = input("Enter authorized administrator(exclude yourself, q to stop): ")
        if auth_admin == "q":
            break
        elif auth_admin == "r" and auth_admins:
            auth_admins.pop()
        else:
            auth_admins.append(auth_admin)

    # Fills list of authorized users
    while True:
        auth_user = input("Enter authorized user(exclude yourself, q to stop): ")
        if auth_user == "q":
            break
        elif auth_user == "r" and auth_users:
            auth_users.pop()
        else:
            auth_users.append(auth_user)

    for current_user in current_users:
        if current_user not in auth_admins and current_user not in auth_users:
            try:
                print("Deleting user " + current_user)
                process = subprocess.Popen(["sudo", "userdel", current_user])
                process.wait()
            except:
                print("Error deleting user")
            current_users.remove(current_user)

    for user in current_users:
        admin = util.is_user_admin(user)
        if admin and user not in auth_admins:
            try:
                process = subprocess.Popen(["sudo", "gpasswd", "-d", user, "sudo"])
                process.wait()
            except:
                print("Error deleting user from group sudo")
        elif not admin and user in auth_admins:
            try:
                process = subprocess.Popen(["sudo", "gpasswd", "-a", user, "sudo"])
                process.wait()
            except:
                print("Error adding user to group sudo")

        process = subprocess.Popen(["sudo", "passwd", user], stdin=subprocess.PIPE)
        process.communicate(f"{SECURE_PASSWORD}\n{SECURE_PASSWORD}\n".encode())
        process.wait()

user_to_add = input("Add user(q to stop): ")
while user_to_add != "q":
    process = subprocess.Popen(["sudo", "useradd", user_to_add])
    process.wait()
    user_to_add = input("Add user(q to stop): ")

# Configure misc security settings
try:
    process = subprocess.Popen(["sudo", "passwd", "-l" "root"]) # Root password is no longer blank
    process.wait()

    process = subprocess.Popen(["sudo", "sed", "-i", "/nullok/d", "/etc/pam.d/common-auth"]) # Null passwords do not authenticate
    process = subprocess.Popen(["sudo", "sed", "-i", "s/.*kernel.randomize_va_space.*/kernel.randomize_va_space=2/g", "/etc/sysctl.conf"]) # Addresss space layout randomization enabled

    process = subprocess.Popen(["sudo", "sysctl", "--system"]) # Refreshes the change above
    process.wait()

    process = subprocess.Popen(["sudo", "echo", "1", ">", "/proc/sys/net/ipv4/tcp_syncookies"]) # IPv4 TCP SYN cookies have been enabled
    process.wait()

    process = subprocess.Popen(["sudo", "sed", "-i", "s/.*net.ipv4.tcp_syncookies./net.ipv4.tcp_syncookies=1*", "/etc/sysctl.d/10-network-security.conf"]) # IPv4 TCP SYN cookies have been enabled at boot
    process.wait()

    process = subprocess.Popen(["sudo", "sysctl", "--system"]) # Refreshes the change above
    process.wait()

    process = subprocess.Popen(["sudo", "chmod", "-R", "640", "/etc/shadow" ]) # Sets secure permissions on shadow file
    process.wait()

except Exception as e:
    print(e)

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
print(END_MSG)