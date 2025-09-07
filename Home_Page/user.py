class User:
    def __init__(self, name, location, phone_no, pin):
        self.name = name.strip()
        self.location = location.strip()
        self.phone_no = phone_no.strip()
        self.pin = pin.strip()

    def __str__(self):
        return f"Name: {self.name}, Location: {self.location}, Phone: {self.phone_no}"
    
class Farmer(User):
    def __init__(self, name, location, phone_no, pin, product_specialty, size_of_farm, role=None):
        super().__init__(name, location, phone_no, pin)
        self.product_specialty = product_specialty.strip()
        self.size_of_farm = size_of_farm
        self.role = role.strip() if role else None

    def __str__(self):
        role = self.role if self.role else "N/A"
        return f"[FARMER] Name: {self.name}, Location: {self.location}, Phone: {self.phone_no}, Product: {self.product_specialty}, Size: {self.size_of_farm}, Role: {role}"
    
class Buyer(User):
    def __init__(self, name, location, phone_no, pin, organization=None):
        super().__init__(name, location, phone_no, pin)
        self.organization = organization.strip() if organization else None

    def __str__(self):
        org = self.organization if self.organization else "N/A"
        return f"[BUYER] Name: {self.name}, Location: {self.location}, Phone: {self.phone_no}, Organization: {self.organization}"
