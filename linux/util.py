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
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError as e:
        print(f'An error occurred while writing to {file_path}: {e}')