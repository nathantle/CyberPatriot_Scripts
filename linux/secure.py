import subprocess

default_users = ["lightdm", "systemd-coredump", "root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "systemd.network", "systemd-resolve", "messagebus", "systemd-timesync", "syslog", "_apt", "tss", "uuidd", "avahi-autoipd", "usbmux", "dnsmasq", "kernoops", "avahi", "cups-pk-helper", "rtkit", "whoopsie", "sssd", "speech-dispatcher", "nm-openvpn", "saned", "colord", "geoclue", "pulse", "gnome-initial-setup", "hplip", "gdm", "_rpc", "statd", "sshd", "systemd-network", "systemd-oom", "tcpdump"]
you = input("Enter your username").lower()
# Manual Tasks - Configure Software and Updates
print("")


proceed = input("Press enter to proceed to updates(q to stop)")
if proceed != "q": 
# Updates
    try:
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "full_upgrade"])
        subprocess.run(["sudo", "apt", "autoremove"])
    except Exception:
        print("Error updating packages")

# Configure Firewall
proceed = input("Press enter to proceed to configuring firewall(q to stop)")
if proceed != "q": 
    try:
        subprocess.run(["sudo", "ufw", "enable"])
    except Exception:
        print("Error configuring firewall")

# Configure ssh
proceed = input("Press enter to proceed to configuring ssh(q to stop)")
if proceed != "q": 
    try:
        # Update and start ssh service
        subprocess.run(["sudo", "apt", "install","ssh"])
        subprocess.run(["sudo", "systemctl", "enable","ssh"])
        subprocess.run(["sudo", "systemctl", "start","ssh"])

        # Disable SSH root login
        subprocess.run(["sudo", "sed", "-i", "'s/PermitRootLogin yes/PermitRootLogin no/g'", "/etc/ssh/sshd_config"])

        # Restart SSH
        subprocess.run(["sudo", "systemctl", "restart", "ssh"])
    except Exception:
        print("Error configuring ssh")

# Handle Users
proceed = input("Press enter to proceed to handle users(q to stop)")
if proceed != "q": 
    try:
        output = subprocess.run("getent passwd | cut -d: -f1", shell=True, stdout=subprocess.PIPE)
        current_users = output.stdout.decode("utf-8").splitlines()
        current_users = list(set(current_users) - set(default_users) - {you})
        current_users.remove(you)
        print(current_users)
    except Exception as e:
        print(e)
        print("Error handling users")