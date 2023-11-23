import basics
import mantasks
import users
import policies
import rm_unauth

def main():
    rm_unauth.understand()
    policies.all()
    basics.all()
    mantasks.all()
    users.all()
    rm_unauth.find_unauth_files()

    print("System secured.")

if __name__ == "__main__":
    main()