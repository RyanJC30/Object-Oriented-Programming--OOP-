# Create a class called shoes
# Add attributes (country, code, product, cost and quantity)
# Add methods to get cost, quantity and add __str__
# create the functions required to manage the shoe company
# create a menu for the functions

from tabulate import tabulate

# Parent class Shoes
class Shoes:

    # Added if the user would like to put a product on sale
    on_sale = False

    # Constructor
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Methods
    def get_cost(self):
        print(self.cost)

    def get_quantity(self):
        print(self.quantity)

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"
    
    def put_on_sale(self):
        self.on_sale = True


# - Lists -
shoes_list = []


# - Functions -

# Function to check if the input is a numerical value
def number_validate_input(user_input):
    try:
        user_input = float(user_input)
        return True
    except ValueError:
        print("Value is not numerical.")
        return False
    

# Updating inventoy.txt file
def updating_file():
    with open('inventory.txt', 'w') as shoes_file:
        shoes_file.write("Country,Code,Product,Cost,Quantity\n")
        for shoe in shoes_list:
            shoes_file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")


# Reads data from inventory.txt and appends it to shoes_list
def read_shoes_data():
    try:
        with open('inventory.txt', 'r') as shoes_file:
            next(shoes_file)  # Skips the first line as they are headings
            shoe_details = [line.strip().split(',') for line in shoes_file]
            for details in shoe_details:
                shoe_object = Shoes(details[0], details[1], details[2], int(details[3]), int(details[4]))
                shoes_list.append(shoe_object)

    # exception handeling incase txt file is deleted or missing or a general exception for reading the file
    except FileNotFoundError:
        print("Error: File 'inventory.txt' not found.")
    except Exception as ex:
        print(f"An error occurred while reading the file: {str(ex)}")

        
# Captures the data of a shoe, creates a shoe object, and appends it to shoes_list
def capture_shoes():
    print("Enter the following information to add a new shoe product:\n")

    # String information
    country = input("Country: ")
    code = input("Code: ")
    product = input("Product: ")

    # Numerical Information
    cost = None
    quantity = None

    while True:
        cost = input("Cost: ")
        if number_validate_input(cost):
            cost = int(cost)
            break

    while True:
        quantity = input("Quantity: ")
        if number_validate_input(quantity):
            quantity = int(quantity)
            break

    shoe_object = Shoes(country, code, product, cost, quantity)
    shoes_list.append(shoe_object)

    updating_file()

    print(f"{product} product has been added")


# Prints the data from shoes_list using __str__ function in a table formnat
def view_all():
    if len(shoes_list) >0:
        print("Shoe products:\n")
        table_data = []

        for shoe in shoes_list:
            row = [shoe.country, shoe.code, shoe.product, f"R{shoe.cost}", shoe.quantity]
            table_data.append(row)

        headers = ["Country", "Code", "Product", "Cost", "Quantity"]
        table = tabulate(table_data, headers, tablefmt="fancy_grid")
        print(table)
    else:
        print("There are no shoes to display")


# looks up the shoe products with the lowest stock and asks the user if they would like more stock then updates the txt file
def re_stock():
    lowest_quantity = None
    lowest_quantity_shoes = []
    for shoe in shoes_list:
        if lowest_quantity is None or shoe.quantity < lowest_quantity:
            lowest_quantity = shoe.quantity
            lowest_quantity_shoes = [shoe]
        elif shoe.quantity == lowest_quantity:
            lowest_quantity_shoes.append(shoe)

    if lowest_quantity_shoes:
        print(f"\nThe following shoe products have the lowest inventory quantity of: {lowest_quantity}")
        for index, shoe in enumerate(lowest_quantity_shoes, 1):
            print(f"{index}: {shoe.product}")

        for shoe in lowest_quantity_shoes:
            restock_choice = ""
            while restock_choice not in ["no", "yes"]:
                restock_choice = input(f"Would you like to restock {shoe.product}? (yes/no): ").lower()
                if restock_choice == "yes":
                    added_stock = input("How much stock would you like to add to the current inventory: ")
                    while not added_stock.isnumeric():
                        print("Invalid input.")
                        added_stock = input("Please enter the quantity you would like to restock: ")

                    added_stock = int(added_stock)
                    shoe.quantity += added_stock

                    # Updating the inventory.txt file with the new quantities
                    updating_file()

                    print(f"Stock for product {shoe.product} has been updated with a current total stock of {shoe.quantity}")
                    break

                elif restock_choice == "no":
                    print(f"{shoe.product} stock has not been restocked.")
                    break

                else:
                    print("Invalid input")
    else:
        print("No shoes in the list.")


# Searches a shoe using shoe code and prints it out
def search_shoe(shoe_code):
    for shoe in shoes_list:
        if shoe_code == shoe.code:
            print(f"""
Country:    {shoe.country}
Code:       {shoe.code}
Product:    {shoe.product}
Cost:       {shoe.cost}
Quantity:   {shoe.quantity}""")
            return

    print(f"Shoe code {shoe_code} does not exist")


# Calculates the value (quantity * cost) for all items and prints in a table format
def value_per_item():
    if len(shoes_list) >0:
        print("Shoe product values report:\n")
        table_data = []
        for shoe in shoes_list:
            value = shoe.cost * shoe.quantity

            row = [shoe.product, f"R{shoe.cost}", shoe.quantity, f"R{value}"]
            table_data.append(row)

        headers = ["Product", "Cost", "Qty", "Value"]
        table = tabulate(table_data, headers, tablefmt="simple")
        print(table)
    else:
        print("There are no shoes to display")

# Finds the product with the highest quantity, asks the user to add it on sale and prints
def highest_qty():
    highest_quantity = None
    highest_quantity_shoes = []
    for shoe in shoes_list:
        if highest_quantity is None or shoe.quantity > highest_quantity:
            highest_quantity = shoe.quantity
            highest_quantity_shoes = [shoe]
        elif shoe.quantity == highest_quantity:
            highest_quantity_shoes.append(shoe)

    if highest_quantity_shoes:
        print(f"\nThe following shoe products have the highest inventory quantity of: {highest_quantity}")
        for index, shoe in enumerate(highest_quantity_shoes, 1):
            print(f"{index}: {shoe.product}")

        for shoe in highest_quantity_shoes:
            sale_choice = ""
            while sale_choice not in ["no", "yes"]:
                sale_choice = input(f"Would you like to put {shoe.product} on sale? (yes/no): ").lower()
                if sale_choice == "yes":
                    print(f"{shoe.product} is on sale")
                    shoe.put_on_sale()

                elif sale_choice == "no":
                    print(f"{shoe.product} has not been put on sale.")
                    break

                else:
                    print("Invalid input")
    else:
        print("No shoes in the list.")


# - Main - 

# Menu
menu = True
read_shoes_data()

# Users menu selection
while True:
    user_choice = input('''\nChoose an option from the menu:
1. Add a new shoe product
2. View all shoes
3. Lowest quantity restock
4. Search for a shoe
5. Shoes value report
6. Highest quantity sale
7. Quit application

Enter selection: ''')
    
    while not number_validate_input(user_choice):
        print("\nPlease enter an option from the menu (1 - 7):")
        user_choice = input("Enter selection: ")
    user_choice = int(user_choice)

    # Add a new shoe product - menu option 1
    if user_choice == 1:
        capture_shoes()

    # View all shoe products - menu option 2
    elif user_choice == 2:
        view_all()

    # Lowest quantity products to restock - menu option 3
    elif user_choice == 3:
        re_stock()
 
    # Search for a shoe product using shoe code - menu option 4
    elif user_choice == 4:
        shoe_code = input("Enter in the shoe code you would like to look up: ")
        search_shoe(f"{shoe_code}")

    # Generates a shoe products value report (quantity x cost) - menu option 5
    elif user_choice == 5:
        value_per_item()
 
    # Highest quantity products for sale - menu option 6
    elif user_choice == 6:
        highest_qty()

    # Quit - menu option 7
    elif user_choice == 7:
        print("Goodbye")
        exit()

    else:
        print("Invalid input.")