from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        """
        In this function, you must initialise the following attributes:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity.
        """

        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_value(self):
        """Return the value of a particular shoe object"""
        return self.quantity * self.cost

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        """Add a code to returns a string representation of a class."""
        return (
            f"Product:  {self.product}\n"
            f"Cost:     {self.cost}\n"
            f"Quantity: {self.quantity}\n"
            f"Code:     {self.code}\n"
            f"Country:  {self.country}"
        )


# =============Shoe list / Global variables===========
# The shoe_list will be used to store a list of objects of shoes.
shoe_list = []
INVENTORY_FILE_NAME = "inventory.txt"


# ==========Functions outside the class==============
def read_shoes_data():
    """Open the inventory file and populate the shoe_list list."""
    try:
        with open(INVENTORY_FILE_NAME, "r") as file:
            for index, line in enumerate(file):
                if (
                    index == 0
                ):  # Skip the first line that contains header information
                    continue

                try:
                    line_elements = line.strip().split(",")
                    if len(line_elements) != 5:
                        raise ValueError(
                            "Shoe data did not contain "
                            "the correct number of items"
                        )

                    country, code, product, cost, quantity = line_elements
                    shoe_list.append(
                        Shoe(country, code, product, int(cost), int(quantity))
                    )

                except ValueError as e:
                    print(f"Skipping bad row data at line {index + 1}: {e}")
                except Exception as e:
                    print(
                        f"Error in file {INVENTORY_FILE_NAME}"
                        f" on line {index + 1}: {e}"
                    )

    except FileNotFoundError:
        print(f"Error: {INVENTORY_FILE_NAME} was not found. ")
    except Exception as e:
        print(f"Unexpected error: {e}.")


def write_shoes_data():
    """Write current data in shoe_list back to the file"""
    if not shoe_list:
        print("Inventory is currently empty.")
        return

    try:
        # Capture the header line so we can write it back to the top
        # of the file. We do this instead of hard coding a header
        # just in case the header ever changes.
        with open(INVENTORY_FILE_NAME, "r") as f:
            first_line = f.readline()

        with open(INVENTORY_FILE_NAME, "w", encoding="utf-8") as f:
            f.write(first_line)
            for shoe in shoe_list:
                f.write(
                    f"{shoe.country},{shoe.code},{shoe.product},"
                    f"{shoe.cost},{shoe.quantity}\n"
                )
    except FileNotFoundError:
        print(f"Unable to find {INVENTORY_FILE_NAME}.")
    except Exception as e:
        print(f"Unexpected error: {e}.")


def validate_numerical_input(message):
    """Ensure the user is entering a numerical value"""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input, please enter a numerical value.")


def capture_shoes():
    """Create a new custom shoe object with user input"""
    country = input("Please enter shoe Country: ")
    code = input("Please enter shoe Code: ")
    product = input("Please enter shoe Product: ")
    cost = validate_numerical_input("Please enter shoe Cost: ")
    quantity = validate_numerical_input("Please enter shoe Quantity: ")

    shoe_list.append(Shoe(country, code, product, cost, quantity))
    write_shoes_data()


def view_all():
    """Display all shoes in the inventory using tabulate"""
    if not shoe_list:
        print("Inventory is currently empty.")
        return

    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    shoe_data = []

    # Create a temporary 2D list of shoe data from shoe objects
    # so tabulate can be used
    for shoe in shoe_list:
        shoe_data.append(
            [shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity]
        )
    print(tabulate(shoe_data, headers))


def re_stock():
    """Find the shoe with the lowest quantity and optionally
    increase its stock"""
    if not shoe_list:
        print("Inventory is currently empty.")
        return

    # Find shoe with the lowest quantity
    lowest_qty_shoe = min(shoe_list, key=lambda shoe: shoe.quantity)

    print("The shoe with the lowest quantity is:")
    print(lowest_qty_shoe)

    add_qty = validate_numerical_input("Enter the amount of shoes to add: ")
    lowest_qty_shoe.quantity += add_qty
    write_shoes_data()


def search_shoe():
    """
    This function will search for a shoe from the list
    using the shoe code and return this object so that it will be printed.
    """
    if not shoe_list:
        print("Inventory is currently empty.")
        return None

    code = input("Please enter the shoe code you wish to search for: ")

    for shoe in shoe_list:
        if shoe.code == code:
            return shoe

    print(f"Shoe code {code} was not found.")
    return None


def value_per_item():
    """
    Print tabulated inventory with the addition of a value column.
    value = cost * quantity
    """
    if not shoe_list:
        print("Inventory is currently empty.")
        return

    headers = ["Country", "Code", "Product", "Cost", "Quantity", "Value"]
    shoe_data = []
    # Create a 2D list from shoe objects so tabulate can be used
    for shoe in shoe_list:
        shoe_data.append(
            [
                shoe.country,
                shoe.code,
                shoe.product,
                shoe.cost,
                shoe.quantity,
                f"${shoe.get_value():,.0f}",
            ]
        )
    print(tabulate(shoe_data, headers))


def highest_qty():
    """
    Find and return the shoe object with the highest quantity

    Returns:
        shoe_list[max_index] (shoe object): A shoe object.
    """
    if not shoe_list:
        return None

    return max(shoe_list, key=lambda shoe: shoe.quantity)


# ==========Main Menu=============
# Create a menu that executes each function above.
# This menu should be inside the while loop. Be creative!


def main_menu():
    while True:
        selection = validate_numerical_input(
            """
Please select from the following options:
1. View all shoes
2. Add another shoe to the inventory
3. Re-stock shoes with low quantity
4. Search for a shoe by shoe code
5. Search for sales
6. List the value per item
7. Exit program
Selection: """
        )
        print("")  # Add blank line after selection entered
        try:
            if selection not in range(1, 8):
                print("Invalid input: Please select from available options.")
                input("Press Enter to continue: ")
                continue
            elif selection == 1:  # View all shoes in inventory
                view_all()

            elif selection == 2:  # Add another shoe
                capture_shoes()

            elif selection == 3:  # Re-stock shoes with the lowest quantity
                re_stock()

            elif selection == 4:  # Search for a shoe by shoe code
                shoe = search_shoe()
                if shoe:
                    print(shoe)

            elif selection == 5:  # Search for sales
                shoe = highest_qty()
                if shoe is None:
                    print("Inventory is currently empty.")
                else:
                    print(
                        "Due to high quantity, "
                        "the following shoe is on sale:"
                    )
                    print(shoe)

            elif selection == 6:
                value_per_item()
            elif selection == 7:  # Exit Program
                return

            input("Press Enter to return to menu: ")

        except Exception as e:
            print(f"An exception was encountered: {e}")


def main():
    read_shoes_data()
    main_menu()


# The following code ensures this modules main() function only runs
# when the module is run directly as in python inventory.py
# This prevents the module from running when it is imported
if __name__ == "__main__":
    main()
