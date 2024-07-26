import subprocess

# Manual Tasks - Configure Software and Updates
print("")

# Updates
try:
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "full_upgrade"])
    subprocess.run(["sudo", "apt", "autoremove"])
except Exception:
    print("Error updating packages")

# 