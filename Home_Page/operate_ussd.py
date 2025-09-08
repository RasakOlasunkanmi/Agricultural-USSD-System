import json
import os
from user import Farmer, Buyer
import pwinput

class Operators:
    def __init__(self, filename="user.json"):
        self.filename = filename
        self.user = {"farmers": {}, "buyers": {}}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.user = json.load(f)
            except (json.JSONDecodeError, ValueError):
                print("user.json compromised, reloading to empty file...")
                self.user = {"farmers": {}, "buyers": {}}
                self._save()

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.user, f, indent=4)

    def _is_valid_name(self, name):
        return isinstance(name, str) and bool(name.strip()) and name.replace(" ", "").replace("-", "").replace("'", "").isalpha()
    
    def _is_valid_location(self, location):
        return isinstance(location, str) and bool(location.strip()) and location.strip() != ""
    
    def _is_valid_phone(self, phone_no):
        return isinstance(phone_no, str) and phone_no.isdigit() and len(phone_no) == 11 and phone_no.startswith("0")
    
    def _is_valid_pin(self, pin):
        return isinstance(pin, str) and pin.isdigit() and len(pin) == 4
    
    def _is_valid_number(self, value):
        return value.isdigit() and int(value) > 0
    
    def farmer_registration(self):
        print("\n*** Farmer Registration ***")

        name = input("Name: ").strip()
        if not self._is_valid_name(name):
            print("Invalid name.")
            return

        location = input("Location: ").strip()
        if not self._is_valid_name(location):
            print("Invalid location.")
            return

        phone_no = input("Enter your Phone number (number must be 11 digits and start with zero(0)): ").strip()
        if not self._is_valid_phone(phone_no):
            print("Invalid phone number.")
            return
        if phone_no in self.user["buyers"] or phone_no in self.user["farmers"]:
            print("Phone number already registered.")
            return

        pin = pwinput.pwinput("Enter your PIN (4 digits): ", mask="*")
        if not self._is_valid_pin(pin):
            print("Invalid PIN.")
            return
        confirm = pwinput.pwinput("Confirm your PIN: ", mask="*")
        if pin != confirm:
            print("PINs do not match.")
            return

        product_specialty = input("Product specialty: ").strip()
        if not self._is_valid_name(product_specialty):
            print("Invalid product specialty.")
            return

        size_of_farm = input("farm size in hectares: ").strip()
        if not self._is_valid_number(size_of_farm):
            print("Invalid farm size, must be a positive number measured in hectares")
            return

        role = input("Role (optional, press Enter to skip): ").strip()
        if role:
            if not self._is_valid_name(role):
                print("Invalid role.")
                return

        self.user["farmers"][phone_no] = {
            "name": name,
            "location": location,
            "phone_no": phone_no,
            "pin": pin,
            "product_specialty": product_specialty,
            "size_of_farm": int(size_of_farm),
            "role": role,
        }
        self._save()
        print("farmer registered successfully!\n")

    def buyer_registration(self):
        print("\n*** Buyer Registration ***")

        name = input("Name: ").strip()
        if not self._is_valid_name(name):
            print("Invalid name.")
            return

        location = input("Location: ").strip()
        if not self._is_valid_name(location):
            print("Invalid location.")
            return

        phone_no = input("Enter your Phone number (number must be 11 digits and start with zero(0)): ").strip()
        if not self._is_valid_phone(phone_no):
            print("Invalid phone number.")
            return
        if phone_no in self.user["buyers"] or phone_no in self.user["farmers"]:
            print("Phone number already registered.")
            return

        pin = pwinput.pwinput("Enter your PIN (4 digits): ", mask="*")
        if not self._is_valid_pin(pin):
            print("Invalid PIN.")
            return
        confirm = pwinput.pwinput("Confirm your PIN: ", mask="*")
        if pin != confirm:
            print("PINs do not match.")
            return

        organization = input("Organization (optional, press Enter to skip): ").strip()
        if organization:
            if not self._is_valid_name(organization):
                print("Invalid organization.")
                return

        self.user["buyers"][phone_no] = {
            "name": name,
            "location": location,
            "phone_no": phone_no,
            "pin": pin,
            "organization": organization,
        }
        self._save()
        print("Buyer registered successfully!\n")

    def show_all_users(self):
        import json, os
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                print("\n*** FULL users.json ***")
                print(json.dumps(data, indent=4)) # pretty print
                print("*************************\n")
        else:
            print("No users.json file found.")
    
    def login(self, phone_no, pin):
        if phone_no in self.user["farmers"]:
            users = self.user["farmers"][phone_no]
            if users.get("pin") == pin:
                return "farmer", Farmer(**users)
        if phone_no in self.user["buyers"]:
            users = self.user["buyers"][phone_no]
            if users.get("pin") == pin:
                return "buyer", Buyer(**users)
        return None, None
    
    def pin_reset(self):
        print("\n*** Reset PIN ***")
        phone_no = input("Enter phone number: ").strip()

        # find the user (buyer or seller)
        user = None
        role = None
        if phone_no in self.user["farmers"]:
            user = self.user["farmers"][phone_no]
            role = "farmer"
        elif phone_no in self.user["buyers"]:
            user = self.user["buyers"][phone_no]
            role = "buyer"

        if not user:
            print("Phone number not found.")
            return

        
        old_pin = pwinput.pwinput("Enter old PIN: ", mask="*")
        if old_pin != user["pin"]:
            print("Old PIN does not match.")
            return

        
        new_pin = pwinput.pwinput("Enter new PIN (4 digits): ", mask="*")
        if not self._is_valid_pin(new_pin):
            print("Invalid PIN format.")
            return

        confirm = pwinput.pwinput("Confirm new PIN: ", mask="*")
        if new_pin != confirm:
            print("PINs do not match.")
            return

        
        user["pin"] = new_pin
        self._save()
        print(f"PIN reset successful for {role}.")
    
    def user_preview(self):
        print("\n*** User Preview ***")
        phone_no = input("Phone number: ").strip()

        if phone_no in self.user["farmers"]:
            user = self.user["farmers"][phone_no]
            role = "farmer"
        elif phone_no in self.user["buyers"]:
            user = self.user["buyers"][phone_no]
            role = "buyer"
        else:
            print("Phone number not found.")
            return

        print(f"\nUser Details ({role.title()}):")
        for key, value in user.items():
            print(f"{key.title()}: {value if value else 'N/A'}")


    def preview_all(self):
        print("\n*** Developer Preview (All Users) ***")
        if not any(self.user.values()):
            print("No users found in the system.")
            return

        for role, group in self.user.items():
            if group:
                print(f"\n{role.upper()}:")
                for phone, user in group.items():
                    print(f" Phone: {phone}")
                    for key, value in user.items():
                        print(f" {key.title()}: {value if value else 'N/A'}")