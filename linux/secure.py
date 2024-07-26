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
        subprocess.run(["sudo", "systemctl", "enable","ssh"])
    except Exception:
        print("Error configuring ssh")