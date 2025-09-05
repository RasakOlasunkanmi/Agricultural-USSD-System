from tabulate import tabulate


USERS = [
    {
        "name": "Aliu",
        "phone": "08033334444",
        "pin": "5678",
        "role": "Buyer",
        "location": "Lagos"
    },
    {
        "name": "Chinedu",
        "phone": "08022221111",
        "pin": "1234",
        "role": "Farmer",
        "location": "Lagos",
        "farm_size": "5 acres",
        "crops": ["Maize", "Cassava"]
    }
]

MARKET_PRICES = {
    "Maize": {"Lagos": 150, "Kano": 120, "Abuja": 140},
    "Cassava": {"Lagos": 90, "Ibadan": 80}
}

HARVESTS = [
    {"farmer_name": "Chinedu", "location": "Lagos", "crop": "Maize", "qty": 200, "price": 150},
    {"farmer_name": "Chinedu", "location": "Lagos", "crop": "Cassava", "qty": 500, "price": 90}
]


# --- Buyer Features ---
def login_buyer(phone, pin):
    """Simple login with error handling"""
    try:
        return next(
            u for u in USERS
            if u["phone"] == phone and u["pin"] == pin and u["role"] == "Buyer"
        )
    except StopIteration:
        return None


def buyer_welcome(buyer):
    try:
        return f"Welcome {buyer['name']}! You are logged in as a Buyer."
    except Exception:
        return "Error: Invalid buyer profile."


def buyer_compare_prices(crop_name):
    try:
        if crop_name not in MARKET_PRICES:
            return f"No price data available for {crop_name}."

        table = [(loc, price) for loc, price in MARKET_PRICES[crop_name].items()]
        return tabulate(table, headers=["Location", "Price"], tablefmt="grid")
    except Exception as e:
        return f"Error comparing prices: {e}"


def buyer_find_farmers_by_location(location):
    try:
        farmers = [
            {
                "name": u["name"],
                "location": u.get("location", ""),
                "farm_size": u.get("farm_size", ""),
                "crops": u.get("crops", []),
                "phone": u["phone"]
            }
            for u in USERS if u.get("role") == "Farmer" and u.get("location") == location
        ]

        if not farmers:
            return f"No farmers found in {location}."

        table = [
            (f["name"], f["location"], f["farm_size"], ", ".join(f["crops"]), f["phone"])
            for f in farmers
        ]
        return tabulate(
            table,
            headers=["Farmer", "Location", "Farm Size", "Crops", "Phone"],
            tablefmt="grid"
        )
    except Exception as e:
        return f"Error finding farmers: {e}"


def buyer_view_produce(location=None):
    try:
        harvests = HARVESTS
        if location:
            harvests = [h for h in harvests if h["location"] == location]

        if not harvests:
            return f"No produce listings{' in ' + location if location else ''}."

        table = [
            (h["farmer_name"], h["location"], h["crop"], h["qty"], h["price"])
            for h in harvests
        ]
        return tabulate(
            table,
            headers=["Farmer", "Location", "Crop", "Qty", "Price"],
            tablefmt="grid"
        )
    except Exception as e:
        return f"Error viewing produce: {e}"


# --- Buyer USSD Menu ---
def run_buyer_demo():
    phone = input("Enter your phone number: ").strip()
    pin = input("Enter your PIN: ").strip()
    buyer = login_buyer(phone, pin)

    if not buyer:
        print("Login failed. Invalid phone or PIN.")
        return

    # Show welcome note
    print(buyer_welcome(buyer))

    # Menu loop
    while True:
        print("\n=== Buyer Menu ===")
        print("1. Compare Prices")
        print("2. Find Farmers by Location")
        print("3. View Produce Listings")
        print("0. Back")
        print("9. Main Menu")
        print("#00. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            crop = input("Enter crop name: ").capitalize()
            print(buyer_compare_prices(crop))

        elif choice == "2":
            location = input("Enter location: ").capitalize()
            print(buyer_find_farmers_by_location(location))

        elif choice == "3":
            yn = input("Do you want to filter by location? (yes/no): ").strip().lower()
            if yn == "yes":
                loc = input("Enter location: ").capitalize()
                print(buyer_view_produce(loc))
            else:
                print(buyer_view_produce())

        elif choice == "0":
            print("Going back (placeholder).")
            break

        elif choice == "9":
            print("Returning to Main Menu (placeholder).")
            break

        elif choice == "#00":
            print("Exiting session. Goodbye!")
            exit(0)

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    run_buyer_demo()
