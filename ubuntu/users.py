import subprocess

def run_command(command):
    # Runs command in terminal
    subprocess.run(command, shell=True, check=True)

def users():
    # Declares lists of authorized admins and authorized users
    authadmns = []
    authusrs = []

    # Loops adding authorized admin
    while True:
        authadmn = input("Enter an authorized admin (press q to stop, r to remove last input)): ").lower()
        if authadmn == "q":
            break
        elif authadmn == "r":
            authadmn.pop()
            continue
        authadmns.append(authadmn) # Adds the authadm variable to the authorized admins array

    # Loops adding authorized users
    while True:
        authusr = input("Enter an authorized user (press q to stop, r to remove last input)): ").lower()
        if authusr == "q":
            break
        elif authusr == "r":
            authusrs.pop()
            continue
        authusrs.append(authusr) # Adds the authusr variable to the authorized users array

    # Cuts the output into parts by ":" and shows only the first part of each line
    process = subprocess.Popen("cut -d: -f1 /etc/passwd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        # Takes each line as one element in the array and adds them all to the array
        ulist = output.decode().splitlines()

        # Asks for the default root user so that the script doesn't mess with the default root user
        defaultuser = input("Enter default root user: ").lower()

        # Declares array of default users that we don't want to mess with
        defaultusrs = ["lightdm", "systemd-coredump", "root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "systemd.network", "systemd-resolve", "messagebus", "systemd-timesync", "syslog", "_apt", "tss", "uuidd", "avahi-autoipd", "usbmux", "dnsmasq", "kernoops", "avahi", "cups-pk-helper", "rtkit", "whoopsie", "sssd", "speech-dispatcher", "nm-openvpn", "saned", "colord", "geoclue", "pulse", "gnome-initial-setup", "hplip", "gdm", "_rpc", "statd", "sshd", "systemd-network", "systemd-oom", "tcpdump"]
        
        # Deletes the default root user from the array
        ulist.remove(defaultuser)

        #Creates new array without the default users
        usrlist = [e for e in ulist if e not in defaultusrs]
    else:
        # If the command doesn't work, return empty array and print that there was an error
        print(f"Error: {error.decode()}")
        return []
    
    newpass = "Cyb3rP@triot24!" # New password variable for next block of code
    # Loops through every user in the user list
    for user in usrlist:
        try:
            if user not in authusrs + authadmns: # If user is not on any of the lists
                run_command(f"sudo deluser {user}") # Deletes the user

            # Sets all users' passwords to newpass
            passwd_process = subprocess.Popen(["sudo", "passwd", user], stdin=subprocess.PIPE, stdout=subprocess.PIPE) 
            passwd_process.communicate(input=f'{newpass}\n{newpass}\n'.encode())

            print(f"Successfully changed password for {user}")

            # Setting correct user permissions
            # Gets users' groups
            process = subprocess.Popen(f"sudo groups {user}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            groups = output.decode().strip().split() # Stores users' groups in an array

            if "sudo" in groups and user not in authadmns: # If they have admin permissions and they are not an authorized admin
                run_command(f"sudo deluser {user} sudo") # Removes the user from group sudo, essentially removing admin permissions
            elif "sudo" not in groups and user in authadmns: # If they do not have admin permissions and they are an authorized admin
                run_command(f"sudo adduser {user} sudo") # Adds the user to group sudo, adding admin permissions
        except Exception:
            print(f"Error occured")

    while True:
        usrtoadd = input("Enter a user to add (press q to stop, r to remove last input)): ").lower()

        if usrtoadd == "q":
            break
        elif usrtoadd == "r":
            usrtoadd.pop()
            continue
        run_command(f"sudo useradd {usrtoadd}")

    run_command("sudo passwd -l root")

def groups():
    while True:
        grouptoadd = input("Enter a group to add (press q to stop, r to remove last input): ").lower()
        if grouptoadd == "q":
            break
        elif grouptoadd == "r":
            grouptoadd.pop()
            continue
        run_command(f"sudo addgroup {grouptoadd}")

def all():
    users()
    groups()