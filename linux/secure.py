import subprocess
import util
default_users = ["lightdm", "systemd-coredump", "root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "systemd.network", "systemd-resolve", "messagebus", "systemd-timesync", "syslog", "_apt", "tss", "uuidd", "avahi-autoipd", "usbmux", "dnsmasq", "kernoops", "avahi", "cups-pk-helper", "rtkit", "whoopsie", "sssd", "speech-dispatcher", "nm-openvpn", "saned", "colord", "geoclue", "pulse", "gnome-initial-setup", "hplip", "gdm", "_rpc", "statd", "sshd", "systemd-network", "systemd-oom", "tcpdump"]
you = input("Enter your username: ").lower()

current_users = []
auth_admins = []
auth_users = []

sec_password = "Cyb3rP@triot25!"

# Manual Tasks - Configure Software and Updates
print("")

proceed = input("Press enter to proceed to updates(q to stop)")
if proceed != "q": 
    # Updates
    try:
        process = subprocess.Popen(["sudo", "apt", "update"])
        process.wait()
        process = subprocess.Popen(["sudo", "apt", "full_upgrade"])
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
        current_users = list(set(current_users) - set(default_users) - {you})
    except Exception as e:
        print(e)
        print("Error handling users")

    while True:
        auth_admin = input("Enter authorized administrator(exclude yourself): ")
        if auth_admin == "q":
            break
        elif auth_admin == "r" and auth_admins:
            auth_admins.pop()
        else:
            auth_admins.append(auth_admin)

    while True:
        auth_user = input("Enter authorized user(exclude yourself): ")
        if auth_user == "q":
            break
        elif auth_user == "r" and auth_users:
            auth_users.pop()
        else:
            auth_users.append(auth_user)

    for current_user in current_users:
        if current_user not in auth_admins and current_user not in auth_users:
            try:
                process = subprocess.Popen(["sudo", "userdel", current_user])
                process.wait()
            except:
                print("Error deleting user")
            current_users.remove(current_user)

    for user in current_users:
        admin = util.is_user_admin(user)
        if admin and user not in auth_admins:
            try:
                process = subprocess.Popen(["sudo", "deluser", user, "sudo"])
                process.wait()
            except:
                print("Error deleting user from group sudo")
        elif not admin and user in auth_admins:
            try:
                process = subprocess.Popen(["sudo", "adduser", user, "sudo"])
                process.wait()
            except:
                print("Error adding user to group sudo")

        process = subprocess.Popen(["sudo", "passwd", user])
        process.communicate(f"{user}:{sec_password}".encode())
        process.wait()