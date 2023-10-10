import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)
def updates():
    packagemgr = input("What package manager do you want to use?(apt/yum/apt-get)")
    run_command("sudo apt update -y")
    run_command("sudo apt upgrade -y")
    run_command("sudo apt autoremove -y")
    run_command("sudo ufw enable")
    run_command("sudo ufw default deny incoming")
    run_command("sudo ufw default allow outgoing")
    run_command("sudo ufw allow ssh")
def services():
    run_command("sudo apt install ssh")

    #Disable SSH root login
    run_command("sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config")
    run_command("sudo service ssh restart")

    print("SSH root login disabled.")

    print("Enforcing SSH key authentication...")

    #Disable password authentication in SSH server configuration
    run_command("sudo sed -i s/PasswordAuthentication yes/PasswordAuthentication no/ /etc/ssh/sshd.config")

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

    moreservices1 == False

    while moreservices1:
        srvc = input("Enter a desired service to delete: ")
        moreservices = input("Done?(y/n)")

        run_command(f"sudo systemctl stop {srvc}")
        run_command(f"sudo systemctl disable {srvc}")
        if moreservices == "y":
            moreservices1 == True
        else:
            moreservices1 == False
def all():
    updates()
    services()