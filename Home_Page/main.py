import pwinput
from operate_ussd import Operators

operation = Operators()

def menu():
    while True:
        print("\n*** USSD Menu ***")
        print("1. Login")
        print("2. Farmer Registration")
        print("3. Buyer Registration")
        print("4. Reset PIN")
        print("5. User Preview")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            phone_no = input("Phone number: ").strip()
            pin = pwinput.pwinput("PIN: ", mask="*")
            role, users = operation.login(phone_no, pin)
            if role:
                print(f"Login successful as {role}!")
                print(users)
            else:
                print("Invalid phone or PIN.")

        elif choice == "2":
            operation.farmer_registration()

        elif choice == "3":
            operation.buyer_registration()

        elif choice == "4":
            operation.pin_reset()

        elif choice == "5":
            operation.user_preview()

        elif choice == "6":
            print("Goodbye")
            break

        elif choice == "7":
            operation.show_all_users()

        elif choice == "10":
            operation.preview_all()

        else:
            print("Invalid option. Please choose 1–6.")

if __name__ == "__main__":
    menu()
