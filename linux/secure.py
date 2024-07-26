import subprocess

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
        output = subprocess.run("getent passwd | cut -d: -f1")
        print(output)
    except:
        print("Error handling users")