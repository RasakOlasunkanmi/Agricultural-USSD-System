import getpass
from operate_ussd import Operators
from user import Farmer, Buyer

def main():
    operation = Operators("user.json")
    while True:
        print("\n***** USSD MENU *****")
        print("1. Login")
        print("2. Farmer Registration")
        print("3. Buyer Registration")
        print("4. Reset PIN")
        print("5. Exit")
        choice = input("Choose an option from 1 to 5: ").strip()
        if choice == "1":
            phone_no = input("Enter phone number: "). strip()
            pin = getpass.getpass("Enter your PIN: ").strip()
            role, user = operation.login(phone_no, pin)
            if role:
                print(f"Login Successful: Welcome, {role}")
                print(user)
            else:
                print("Invalid Phone number or PIN.")

        elif choice == "2":
            name = input("Enter your name: ").strip()
            location = input("Enter your location: ").strip()
            phone_no = input("Enter your phone number (11 digits): ").strip()
            pin = getpass.getpass("Enter your PIN (4 digits): ").strip()
            confirm_pin = getpass.getpass("Confirm your PIN: ").strip()
            if pin != confirm_pin:
                print("PINs do not match, check again")
                continue
            product_specialty = input("Enter farm product to sell: ").strip()
            size_of_farm = input("Enter your farm size in hectares: ").strip()
            role = input("Enter role (Optional, press Enter to skip: ").strip() or None
            farmer = Farmer(name, location, phone_no, size_of_farm, product_specialty, size_of_farm, role)
            success, message = operation.farmer_registration(farmer)
            print(message)

        elif choice == "3":
            name = input("Enter your name: ").strip()
            location = input("Enter your location: ").strip()
            phone_no = input("Enter phone number (11 digits): ").strip()
            pin = getpass.getpass("Enter PIN (4 digits): ").strip()
            confirm_pin = getpass.getpass("Confirm PIN: ").strip()
            if pin != confirm_pin:
                print("PINs do not match, check again")
                continue
            org = input("Enter organization name (Optional, press Enter to Skip): ").strip() or None
            buyer = Buyer(name, location, phone_no, pin, org)
            success, message = operation.buyer_registration(buyer)
            print(message)

        elif choice == "4":
            phone_no = input("Enter your phone number: ").strip()
            new_pin = getpass.getpass("Enter NEW PIN (4 digits): ").strip()
            confirm_pin = getpass.getpass("Confirm NEW PIN: ").strip()
            if new_pin != confirm_pin:
                print("PINs do not match, Try Again")
                continue
            success, message = operation.pin_reset(phone_no, new_pin)
            print(message)

    else:
            print("Invalid Option, Please choose between 1 to 5")

if __name__=="__main__":
        main()