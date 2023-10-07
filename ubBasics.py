import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def updates():
    run_command("sudo apt update -y")
    run_command("sudo apt upgrade -y")
    run_command("sudo apt autoremove -y")
    run_command("sudo ufw enable")
    run_command("sudo ufw allow ssh")

def services():
    run_command("sudo apt install ssh")

    print("Disabling SSH root login...")

    #Back up SSH config file
    run_command("sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")

    #Open SSH config file for editing
    with open("/etc/ssh/sshd_config", "r") as f:
        lines = f.readlines()

    #Update SSH configuration
    updated_lines = []
    for line in lines:
        if line.startswith("PermitRootLogin"):
            updated_lines.append("PermitRootLogin no/n")
        else:
            updated_lines.append(line)

    #Write updating configuration to file
    with open("/etc/ssh/sshd_config", "w") as f:
        f.writelines(updated_lines)

    #Restart SSH service
    run_command("sudo service ssh restart")

    print("SSH root login disabled.")

    print("Enforcing SSH key authentication...")

    #Disable password authentication in SSH server configuration
    run_command("sudo sed -i s/#PasswordAuthentication yes/PasswordAuthentication no/ /etc/ssh/sshd.config")

    #Restart SSH service
    run_command("sudo systemctl restart ssh")

    print("SSH key based authentication has been enforced.")

    run_command("sudo apt purge -y telnet ftp telnetd vsftpd")

    command = "systemctl list-units --type=service --state=running --no-pager --plain --no-legend"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()

    services = output.decode().strip().split("\n")

    for service in services:
        print(service)

    anymoreservices == False

    while anymoreservices == False:
        srvc = input("Enter a desired service to delete: ")
        moreservices = input("Done?(y/n)")

        run_command(f"sudo systemctl stop {srvc}")
        run_command(f"sudo systemctl disable {srvc}")
        if moreservices == "y":
            anymoreservices == True
        else:
            anymoreservices == False

def users():
    done = False

    authadmns = []
    authusrs = []

    while(done != True):
        authadmn = input("Enter an authorized admin: ")
        authadmns.append(authadmn)
        bo = input("Done?(y/n)").lower()
        if(bo == "y"):
            done = True
        else:
            done = False
    done = False
    while(done != True):
        authusr = input("Enter an authorized user: ")
        authusrs.append(authusr)
        bo = input("Done?(y/n)").lower()
        if(bo == "y"):
            done = True
        else:
            done = False
    

    process = subprocess.Popen("cut -d: -f1 /etc/passwd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        ulist = output.decode().splitlines()
        defaultuser = input("Enter default root user: ").lower()
        defaultusrs = ["root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "systemd.network", "systemd-resolve", "messagebus", "systemd-timesync", "syslog", "_apt", "tss", "uuidd", "avahi-autoipd", "usbmux", "dnsmasq", "kernoops", "avahi", "cups-pk-helper", "rtkit", "whoopsie", "sssd", "speech-dispatcher", "nm-openvpn", "saned", "colord", "geoclue", "pulse", "gnome-initial-setup", "hplip", "gdm", "_rpc", "statd", "sshd", "systemd-network", "systemd-oom", "tcpdump"]
        ulist.remove(defaultuser)
        usrlist = [e for e in ulist if e not in defaultusrs]
    else:
        print(f"Error: {error.decode()}")
        return []
    
    command = "grep '^sudo:.*$' /etc/group | cut -d: -f4"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    admins = output.decode().strip().split(",")
    admins.remove(defaultuser)

    for user in usrlist:
        if user not in authusrs + authadmns:
            run_command(f"sudo deluser {user}")
        newpass = "Cyb3rP@triot24!"
        passwd_process = subprocess.Popen(['sudo', 'passwd', user], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        passwd_process.communicate(input=f'{newpass}\n{newpass}\n'.encode())

        # Check the exit code to determine if the password change was successful
        if passwd_process.returncode == 0:
            print(f"Password changed successfully for user '{user}'")
        else:
            print(f"Failed to change password for user '{user}'")
        
        #Setting correct user permissions
        process = subprocess.Popen(f"sudo groups {user}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()
        groups = output.decode().strip().split()

        if "sudo" in groups:
            sudoer = True
        else:
            sudoer = False

        if sudoer and user not in authadmns:
            run_command(f"sudo adduser {user} sudo")
        elif not sudoer and user in authadmns:
             run_command(f"sudo deluser {user} sudo")
             
    run_command("sudo passwd -l root")