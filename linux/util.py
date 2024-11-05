import subprocess

def is_user_admin(user):
    try:
        process = subprocess.Popen(["sudo", "groups", user], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if "sudo" in output.decode("utf-8").split():
            return True
        else:
            return False
    except Exception as e:
        print(e)

def write_to_file(file_path, content):
    subprocess.run(f"sudo echo \"{content}\" > {file_path}", shell=True)