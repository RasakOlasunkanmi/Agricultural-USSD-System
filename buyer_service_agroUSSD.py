from tabulate import tabulate

# Users: A buyer and a farmer
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

# Market prices for crops across different locations
MARKET_PRICES = {
    "Maize": {"Lagos": 150, "Kano": 120, "Abuja": 140},
    "Cassava": {"Lagos": 90, "Ibadan": 80}
}

# Harvests: produce listings from farmers
HARVESTS = [
    {"farmer_name": "Chinedu", "location": "Lagos", "crop": "Maize", "qty": 200, "price": 150},
    {"farmer_name": "Chinedu", "location": "Lagos", "crop": "Cassava", "qty": 500, "price": 90}
]


# --- Buyer Features ---
def login_buyer(phone, pin):
    """Login function for buyers with error handling"""
    try:
        # Find a buyer that matches phone, pin, and role = Buyer
        return next(
            u for u in USERS
            if u["phone"] == phone and u["pin"] == pin and u["role"] == "Buyer"
        )
    except StopIteration:
        return None    # No match found


def buyer_welcome(buyer):
    # Return a welcome message for the buyer
    try:
        return f"Welcome {buyer['name']}! You are logged in as a Buyer."
    except Exception:
        return "Error: Invalid buyer profile."


def buyer_compare_prices(crop_name):
    # Compare crop prices across locations
    try:
        if crop_name not in MARKET_PRICES:
            return f"No price data available for {crop_name}."

        # Create a table of locations and prices
        table = [(loc, price) for loc, price in MARKET_PRICES[crop_name].items()]
        return tabulate(table, headers=["Location", "Price"], tablefmt="grid")
    except Exception as e:
        return f"Error comparing prices: {e}"


def buyer_find_farmers_by_location(location):
    # Find farmers located in a given location
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
    # View available produce listings, optionally filtered by location
    try:
        harvests = HARVESTS
        if location:     # Filter if location is provided
            harvests = [h for h in harvests if h["location"] == location]

        if not harvests:
            return f"No produce listings{' in ' + location if location else ''}."

        # Create a table of produce listings
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
    # Interactive menu for buyers
    # Step 1: Login
    phone = input("Enter your phone number: ").strip()
    pin = input("Enter your PIN: ").strip()
    buyer = login_buyer(phone, pin)

    if not buyer:
        print("Login failed. Invalid phone or PIN.")
        return

    # Step 2: Show welcome message
    print(buyer_welcome(buyer))

    # Step 3: Menu loop
    while True:
        print("\n=== Buyer Menu ===")
        print("1. Compare Prices")
        print("2. Find Farmers by Location")
        print("3. View Produce Listings")
        print("0. Back")
        print("9. Main Menu")
        print("#00. Exit")

        choice = input("Select option: ").strip()
        
        # Compare Prices
        if choice == "1":
            crop = input("Enter crop name: ").capitalize()
            print(buyer_compare_prices(crop))

        # Find Farmers
        elif choice == "2":
            location = input("Enter location: ").capitalize()
            print(buyer_find_farmers_by_location(location))

        # View Produce Listings
        elif choice == "3":
            yn = input("Do you want to filter by location? (yes/no): ").strip().lower()
            if yn == "yes":
                loc = input("Enter location: ").capitalize()
                print(buyer_view_produce(loc))
            else:
                print(buyer_view_produce())

        # Back to previous menu
        elif choice == "0":
            print("Going back (placeholder).")
            break
        
        # Return to main menu    
        elif choice == "9":
            print("Returning to Main Menu (placeholder).")
            break
        
        # Exit system    
        elif choice == "#00":
            print("Exiting session. Goodbye!")
            exit(0)

        # Invalid option
        else:
            print("Invalid option. Try again.")

# Run the demo if script is executed directly
if __name__ == "__main__":
    run_buyer_demo()
    
    
    
    
    """
    Summary of the Code

This Python script simulates a USSD-like Buyer system for an agricultural marketplace.

- There are users (buyers and farmers), market prices, and harvest data.

- A buyer logs in with a phone number and PIN.

- Once logged in, the buyer has menu options to:

    1) Compare market prices of crops across locations.

    2) Find farmers by location.

    3) View available produce listings (with optional location filter).

The system uses the tabulate library to neatly display tables.

Basic error handling is included to prevent crashes.
    """