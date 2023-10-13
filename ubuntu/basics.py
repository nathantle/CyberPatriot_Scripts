import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)
def updates():
    packagemanager = ""
    while packagemanager != "apt" and packagemanager != "yum" and packagemanager != "apt-get":
        try:
            packagemanager = input("Enter the package manager this system uses (apt, yum, apt-get): ").lower()
            if packagemanager != "apt" and "yum" and "apt-get":
                print("Enter a valid package manager. ")
        except ValueError:
            print("Enter a valid value.")
    if packagemanager == "apt":     
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

    print("SSH root login disabled.")

    # print("Enforcing SSH key authentication...")

    #Disable password authentication in SSH server configuration
    # This code does not work
    # run_command("sudo sed -i s/PasswordAuthentication yes/PasswordAuthentication no/ /etc/ssh/sshd.config")

    #Restart SSH service
    run_command("sudo service ssh restart")

    run_command("sudo apt purge -y telnet ftp telnetd vsftpd")

    command = "systemctl list-units --type=service --state=running --no-pager --plain --no-legend"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()

    services = output.decode().strip().split("\n")

    for service in services:
        print(service)
    
    badServices = ["nginx", "apache2"]

    for badService in badServices:
        run_command(f"sudo systemctl stop {badService}")
        run_command(f"sudo systemctl disable {badService}")

    while True:
        srvc = input("Enter a desired service to delete(q to stop): ")

        if srvc == "q" or "Q":
            break

        run_command(f"sudo systemctl stop {srvc}")
        run_command(f"sudo systemctl disable {srvc}")
def all():
    updates()
    services()