import subprocess

def is_user_admin(user):
    try:
        process = subprocess.Popen(["sudo", "groups", user], stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.split(" ")
        if "sudo" in output.decode("utf-8"):
            return True
        else:
            return False
    except:
        print("error")