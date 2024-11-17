'''
CyberPatriot Windows Script
Written by Nathan Le

Designed to fix security issues and earn points in the CyberPatriot Competition
'''
import subprocess

# Tuple of default users that should not be modified
DEFAULT_USERS = ()

# Tuple of common unauthorized services
BAD_SERVICES = ()

# String that stores the user account that should not be modified
YOU = input("Enter your username: ")

# Declare lists to store current users, authorized admins and users
current_users = []
auth_admins = []
auth_users = []

# Final string that stores a secure password
SECURE_PASSWORD = "Cyb3rP@triot25!"

# Configure firewall
proceed = input("Press enter to proceed to configuring firewall(s to skip)").lower()
if proceed != "s":
    try:
        subprocess.run("netsh advfirewall set allprofiles state on", shell=True)
    except Exception as e:
        print(e)

# Handle users
