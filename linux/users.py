import subprocess

def run_command(command):
    # Runs command in terminal
    subprocess.run(command, shell=True, check=True)
def clear():
    run_command("clear")

def users():
    next_step = input("Press enter to proceed to next step(managing users), type 'skip' to skip this step")
    if next_step == "skip":
        return   
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
    usrlist = subprocess.run(["cut", "-d:", "-f1", "/etc/passwd"], capture_output=True, text=True).stdout.split()

    # Asks for the default root user so that the script doesn't mess with the default root user
    defaultusr = input("Enter default root user: ").lower()

    # Declares array of default users that we don't want to mess with
    defaultusrs = ["lightdm", "systemd-coredump", "root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "systemd.network", "systemd-resolve", "messagebus", "systemd-timesync", "syslog", "_apt", "tss", "uuidd", "avahi-autoipd", "usbmux", "dnsmasq", "kernoops", "avahi", "cups-pk-helper", "rtkit", "whoopsie", "sssd", "speech-dispatcher", "nm-openvpn", "saned", "colord", "geoclue", "pulse", "gnome-initial-setup", "hplip", "gdm", "_rpc", "statd", "sshd", "systemd-network", "systemd-oom", "tcpdump"]
    usrlist.remove(defaultusr) # Deletes the default root user from the list

    for defaultusr in defaultusrs:
        try:
            usrlist.remove(defaultusr)
        except ValueError:
            continue

    for usr in usrlist: # Loops through every user in the user list
        try:
            if usr not in authusrs + authadmns: # If user is not on any of the lists
                print(f"Deleting {usr}")
                run_command(f"sudo deluser {usr}") # Deletes the user

            # Sets all users' passwords to newpass
            subprocess.run(["passwd", usr], input=b"Cyb3rP@triot24!\nCyb3rP@triot24!\n", check=True)
            print(f"Successfully changed password for {usr}")

            # Setting correct user permissions
            # Gets users' groups
            groups = subprocess.run(["groups", usr], capture_output=True, text=True).stdout.split()

            if "sudo" in groups and usr not in authadmns: # If they have admin permissions and they are not an authorized admin
                print(f"Removing {usr} from group 'sudo'")
                run_command(f"sudo deluser {usr} sudo") # Removes the user from group sudo, essentially removing admin permissions
            elif "sudo" not in groups and usr in authadmns: # If they do not have admin permissions and they are an authorized admin
                print(f"Adding {usr} to group 'sudo'")
                run_command(f"sudo adduser {usr} sudo") # Adds the user to group sudo, adding admin permissions
        except Exception as e:
            print(f"Error occured: {e}")

    for authadm in authadmns:
        if authadm not in usrlist:
            subprocess.run(["sudo", "adduser", authadm], input=b"Cyb3rP@triot24!\nCyb3rP@triot24!\n\n\n\n\n\n\n")
    for authusr in authusrs:
        if authusr not in usrlist:
            subprocess.run(["sudo", "adduser", authusr], input=b"Cyb3rP@triot24!\nCyb3rP@triot24!\n\n\n\n\n\n\n")

    while True:
        usrtoadd = input("Enter a user to add (press q to stop, r to remove last input)): ").lower()

        if usrtoadd == "q":
            break
        elif usrtoadd == "r":
            usrtoadd.pop()
            continue
        run_command(f"sudo useradd {usrtoadd}")

    run_command("sudo passwd -l root")
    clear()
    print("Users managed")

def groups():
    next_step = input("Press enter to proceed to next step(managing groups), type 'skip' to skip this step")
    if next_step == "skip":
        return   
    while True:
        grouptoadd = input("Enter a group to add (press q to stop, r to remove last input): ").lower()
        if grouptoadd == "q":
            break
        elif grouptoadd == "r":
            grouptoadd.pop()
            continue
        run_command(f"sudo addgroup {grouptoadd}")
    while True:
        grouptorm = input("Enter a group to remove (q to stop): ").lower()
        if grouptorm == "q":
            break
        run_command(f"sudo delgroup {grouptorm}")
    while True:
        usertoaddtogroup = input("Enter a user to add to a group (q to stop) ex: 'group user'\t").lower()
        if usertoaddtogroup == "q":
            break
        usertoaddtogroup = usertoaddtogroup.split()
        run_command(f"sudo adduser {usertoaddtogroup[1]} {usertoaddtogroup[0]}")
    clear()
    print("Groups managed")

def all():
    users()
    groups()