import subprocess

def run_command(command):
    # Runs command in terminal
    subprocess.run(command, shell=True, check=True)

def users():
    done = False

    # Declares lists of authorized admins and authorized users
    authadmns = []
    authusrs = []

    # Loops adding authorized admin
    while not done:
        authadmn = input("Enter an authorized admin: ")

        # Adds the authadm variable to the authorized admins array
        authadmns.append(authadmn)

        # Asks the user if they are done listing admins
        donelistingadmins = input("Done?(y/n)").lower()
        if(donelistingadmins == "y"):
            done = True
        else:
            done = False
    done = False

    # Loops adding authorized users
    while not done:
        authusr = input("Enter an authorized user: ")

        # Adds the authusr variable to the authorized users array
        authusrs.append(authusr)

        # Asks the user if they are done listing users
        donelistingusers = input("Done?(y/n)").lower()
        if donelistingusers == "y":
            done = True
        else:
            done = False

    # Cuts the output into parts by ":" and shows only the first part of each line
    process = subprocess.Popen("cut -d: -f1 /etc/passwd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        # Takes each line as one element in the array and adds them all to the array
        ulist = output.decode().splitlines()

        # Asks for the default root user so that the script doesn't mess with the default root user
        defaultuser = input("Enter default root user: ").lower()

        # Declares array of default users that we don't want to mess with
        defaultusrs = ["root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "systemd.network", "systemd-resolve", "messagebus", "systemd-timesync", "syslog", "_apt", "tss", "uuidd", "avahi-autoipd", "usbmux", "dnsmasq", "kernoops", "avahi", "cups-pk-helper", "rtkit", "whoopsie", "sssd", "speech-dispatcher", "nm-openvpn", "saned", "colord", "geoclue", "pulse", "gnome-initial-setup", "hplip", "gdm", "_rpc", "statd", "sshd", "systemd-network", "systemd-oom", "tcpdump"]
        
        # Deletes the default root user from the array
        ulist.remove(defaultuser)

        #Creates new array without the default users
        usrlist = [e for e in ulist if e not in defaultusrs]
    else:
        # If the command doesn't work, return empty array and print that there was an error
        print(f"Error: {error.decode()}")
        return []

    # Loops through every user in the user list
    for user in usrlist:
        if user not in authusrs + authadmns: # If user is not on any of the lists
            run_command(f"sudo deluser {user}") # Deletes the user

        # Sets all users' passwords to newpass
        passwd_process = subprocess.Popen(['sudo', 'passwd', "Cyb3rP@triot24!"], stdin=subprocess.PIPE, stdout=subprocess.PIPE) 
        passwd_process.communicate(input=f'{"Cyb3rP@triot24!"}\n{"Cyb3rP@triot24!"}\n'.encode())

        # Check the exit code to determine if the password change was successful
        if passwd_process.returncode == 0:
            print(f"Password changed successfully for user '{user}'")
        else:
            print(f"Failed to change password for user '{user}'")
        
        # Setting correct user permissions
        # Gets users' groups
        process = subprocess.Popen(f"sudo groups {user}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()
        groups = output.decode().strip().split() # Stores users' groups in an array

        if "sudo" in groups: # If groups contains "sudo"
            sudoer = True
        else:
            sudoer = False

        if sudoer and user not in authadmns: # If they have admin permissions and they are not an authorized admin
            run_command(f"sudo deluser {user} sudo") # Removes the user from group sudo, essentially removing admin permissions
        elif not sudoer and user in authadmns: # If they do not have admin permissions and they are an authorized admin
            run_command(f"sudo adduser {user} sudo") # Adds the user to group sudo, adding admin permissions

    doneaddingusers = False

    while not doneaddingusers:
        wanttoaddusers = input("Add a user(y/n)").lower()
        if wanttoaddusers == "y":
            usertoadd = input("Enter name of user to add: ")
            run_command(f"sudo adduser {usertoadd}")
            moreuserstoadd = input("Any more?(y/n)")
            if moreuserstoadd == "y":
                doneaddingusers = False
            else:
                doneaddingusers = True
        else:
            doneaddingusers = True

    run_command("sudo passwd -l root")

def groups():
    doneaddinggroups = False

    while not doneaddinggroups:
        grouptoadd = input("Enter the name of the group to add:")
        run_command(f"sudo addgroup {grouptoadd}")

        doneaddinguserstogroup = False

        while(not doneaddinguserstogroup):
            usertoadd = input("Enter the name of the user to add to the group:")
            run_command(f"sudo useradd {usertoadd} {grouptoadd}")
            finishedaddinguserstogroup = input("Any more users?(y/n)").lower()
        if finishedaddinguserstogroup == "y":
            doneaddinguserstogroup = True
        else:
            doneaddinguserstogroup = False
        finishedaddinggroups = input("Add another group?(y/n)").lower()
        if finishedaddinggroups == "y":
            doneaddinggroups == True
        else:
            doneaddinggroups == False

def all():
    users()
    groups()