import basics
import mantasks
import users
import policies
import rm_unauth

def main():
    basics.all()
    mantasks.all()
    users.all()
    policies.all()
    rm_unauth.understand()

    print("System secured.")

if __name__ == "__main__":
    main()