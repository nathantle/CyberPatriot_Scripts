import basics
import mantasks
import users
import policies
import rm_unauth

def main():
    rm_unauth.understand()
    basics.all()
    mantasks.all()
    users.all()
    policies.all()
    rm_unauth.find_unauth_files()

    print("System secured.")

if __name__ == "__main__":
    main()