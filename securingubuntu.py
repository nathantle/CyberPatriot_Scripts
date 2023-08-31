import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def update_packages():
    print("Updating packages...")
    run_command("sudo apt update -y")
    run_command("sudo apt upgrade -y")
    run_command("sudo apt autoremove -y")
    print("Updated packages.")

def configure_firewall():
    print("Configuring firewall...")
    run_command("sudo ufw default deny incoming")
    run_command("sudo ufw default allow outgoing")
    run_command("sudo ufw allow ssh")
    run_command("sudo ufw enable")
    print("Firewall configured")

def disable_ssh_root_login():
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

    print("Root login disabled.")

def main():
    disable_ssh_root_login()
    print("System secured.")

if __name__ == "__main__":
    main()