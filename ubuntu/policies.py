import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def passwd_policies():
    print("Setting password policies...")

    run_command("sudo sed -i 's/^PASS_MAX\_REPEATS.*/PASS_MAX_REPEATS\t5/' /etc/login.defs")
    run_command("sudo sed -i 's/^PASS\_MAX\_DAYS.*/PASS_MAX_DAYS\t90/' /etc/login.defs")
    run_command("sudo sed -i 's/^PASS\_MAX\_DAYS\_ADMIN.*/PASS_MAX_DAYS_ADMIN\t30/' /etc/login.defs")
    run_command("sudo sed -i 's/^PASS\_MIN\_DAYS.*/PASS_MIN_DAYS\t15/' /etc/login.defs")
    run_command("sudo sed -i 's/^PASS\_MIN\_LEN.*/PASS_MIN_LEN\t10/' /etc/login.defs")

    run_command("sudo apt install libpam-pwquality")
    # Require password complexity - enabled
    run_command("sudo sed -i 's/^password.*requisite.*pam_pwquality\.so.*/password requisite pam_pwquality.so try_first_pass retry=3 minlen=10 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1/' /etc/pam.d/common-password")


def all():
    passwd_policies()