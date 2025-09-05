import json
import os
from user import Farmer, Buyer

class Operators:
    def __init__(self, filename="user.json"):
        self.filename = filename
        self.user = {"Farmers": {}, "Buyers": {}}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.user = json.load(f)
            except json.JSONDecodeError:
                print("user.json compromised, reloading...")
                self.user = {"Farmers": {}, "Buyers": {}}
                self.save()

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.user, f, indent=4)

    def _is_valid_name(self, name):
        return isinstance(name, str) and name.replace(" ", "").replace("-", "").replace("'", "").isalpha()
    
    def _is_valid_location(self, location):
        return isinstance(location, str) and location.strip() != ""
    
    def _is_valid_phone(self, phone_no):
        return phone_no.isdigit() and len(phone_no) == 11 and phone_no.startswith("0")
    
    def _is_valid_pin(self, pin):
        return pin.isdigit() and len(pin) == 4
    
    def farmer_registration(self, farmer: Farmer):
        if not (self._is_valid_name(farmer.name) and self._is_valid_location(farmer.location) and self._is_valid_phone(farmer.phone_no) and self._is_valid_pin(farmer.pin)):
            return False, "Invalid input!!!"
        if farmer.phone_no in self.user["buyers"] or farmer.phone_no in self.user["farmers"]:
            return False, "Phone have been registered already!!!"
        self.user["farmers"][farmer.phone_no] = farmer.__dict__
        self.save()
        return True, "Farmer registration successful."
    
    def buyer_registration(self, buyer: Buyer):
        if not (self._is_valid_location(buyer.name) and self._is_valid_location(buyer.location) and self._is_valid_phone(buyer.phone_no) and self._is_valid_pin(buyer.pin)):
            return False, "Invalid input!!!"
        if buyer.phone_no in self.user["buyers"] or buyer.phone_no in self.user["farmers"]:
            return False, "Phone number already used!!!"
        self.user["buyers"][buyer.phone_no] = buyer.__dict__
        self.save()
        return True, "Buyer registration successful"
    
    def login(self, phone_no, pin):
        if phone_no in self.user["farmers"]:
            users = self.user["farmers"][phone_no]
            if users["pin"] == pin:
                return "farmer", Farmer(**users)
        elif phone_no in self.user["buyers"]:
            users = self.user["buyers"][phone_no]
            if users["pin"] == pin:
                return "buyer", Buyer(**users)
        return None, None
    
    def pin_reset(self, phone_no, new_pin):
        if not self._is_valid_pin(new_pin):
            return False, "Invalid PIN Format."
        if phone_no in self.user["farmers"]:
            self.user["farmers"][phone_no]["pin"] = new_pin
            self.save()
            return True, "Successfully reset Farmer PIN"
        if phone_no in self.user["buyers"]:
            self.user["buyers"][phone_no]["pin"] = new_pin
            self.save()
            return True, "Successfully reset Buyer PIN"
        return False, "Phone number not found."