import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from termcolor import colored

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("pizza_ordering_system_data")

# link to order sheet
menu = SHEET.worksheet("menu")

# all the order sheet data
menu_data = menu.get_all_values()


def pizza_option_user_input_validator():
    """Check if user has inputted valid data & let them know if they have not
    Args:
        data (str): _description_ the numerical option the user takes whether it's 1-5
        for pizza or 1-10 for quantity.
        input_identity (string) _description_ returns a value so the validator knows if it's validating
        user input for pizza selection or user input for quantity selection

    Returns:
        _type_: boolean_description_if no errors returns True
    """
    
    #infinite loop thats only broken if valid input is given
    while (True):
        try:
            #code that might crash
            pizza_option = pizza_option_input()
            pizza_name, pizza_price = get_pizza_name_and_price_ordered(pizza_option)
            if int(pizza_option) >= 1 and int(pizza_option) <= 5:
                print(f"You have chosen {pizza_name} at a cost of €{pizza_price}")
                quantity_user_input_validator()
                break #exit the immediate loop
            
        except ValueError as e:
            print(f"\nInvalid pizza option entry: {e}, please try again\n")
            print('not a number between 1 and 5')
        #check the while condition if true repeat
        
                
def quantity_user_input_validator():
    """Check if user has inputted valid data & let them know if they have not
    Args:
        pizza_quantity (str): _description_ the numerical option the use it's 1-10 for quantity.
        i
    Returns:
        _type_: boolean_description_if no errors returns True
    """
    #infinite loop thats only broken if valid input is given
    
    while (True):
        try:
            pizza_quantity = order_quantity()
            #code that might crash
            if int(pizza_quantity) >= 1 and int(pizza_quantity) <= 10:
            # add the quantity order to the add to sheet function
                break #exit the immediate loop

        except ValueError as e1:
                    
            print(f"\nInvalid quantity entry: {e1}, please try again\n")
            print("Must be a number between 1 and 10")
                    
        #check the while condition if true repeat

def get_pizza_name_and_price_ordered(pizza_option):
    """_summary_

    Returns:
        : _description_a string of the name of the pizza chosen by the user.
        Passes these values back to where they were called in the main function
    """
    i = pizza_option
    pizza_option = menu.cell(i, 2).value
    pizza_price = menu.cell(i, 3).value
    return pizza_option, pizza_price


def add_to_order_sheet(*data: str):
    """
    *arg used here so I don't have to put in a specific amount of arguments & thus
    would have to make several similar add functions
    To differenciate between the pizza selection input and quantity here
    each tuple item is looped through. If it's length is less than 2 not a word, so
    it's the quantity selection which will either have a length of 1 (nums 1 -9) or 2 for '10'
    """
    order = SHEET.worksheet("order")

    for item in data:
        if len(data[0]) > 2:
            # iterator is length of columns + 1 so new row entered each time
            i = len(order.col_values(1)) + 1
            order.update_cell(i, 1, f"{data[0]}")
            order.update_cell(i, 2, f"{data[1]}")
            break

        if len(data[0]) <= 2:
            # iterator already updated by 1 above so no need for +1 here
            i = len(order.col_values(1))
            quantity_selection = list(item)
            order.update_cell(i, 3, f"{quantity_selection[0]}")
            total_price(quantity_selection[0])
            break


def initial_screen_display():
    """content for initial user interaction with system
    display table with menu to user"""

    print("\033[1m" + "Welcome to " + colored("Nags with Notions!", "red") + "\033[0m")
    print("\nPlease select one of the 5 number options below")

    print(
        tabulate(
            menu_data,
            headers=["Option", "Name", "Price(€)"],
            numalign="center",
            tablefmt="double_outline",
        ),
    )


def pizza_option_input() -> str:
    """create a function to get users pizza choice, return it to the calling function
    which is called in main()
    """
    pizza_option_number = input("Enter a number between 1 and 5 here:\n")
    # TODO: need to implement a clear timer here import timer & os system modules

    return pizza_option_number


def order_quantity():
    """create a function to get users quantity choice, return it to the calling function
    which is called in main()
    """
    order_quantity1 = input("\033[1m" + "Enter a number between 1 and 10 here:\n")
    return order_quantity1


def total_price(quantity: str) -> int:
    """function to calculate total price. Quantity taken from add values function. Quantity argument
    then multiplied with corresponding price in excel sheet. Total price then added to total price column
    in excel

    Args:
        quantity (string): Users selection of amount of pizzas required.
    """
    order = SHEET.worksheet("order")
    i = len(order.col_values(1))
    price = order.cell(i, 2).value
    total = int(quantity) * int(price)
    order.update_cell(i, 4, f"{total}")
    return total


def stock_checker(pizza_option, quantity):
    """function takes in the order and reduces this from the stock. If
    the stock is below 0 the user is informed that the products unavailable
    and to try something else

    Args:
        quantity (int): take from user_order_quantity request function
        pizza_name (int): _description_ taken from user_order_quantity request function

    Returns:
        int: an identifer for which pizza needs to have its stock reduced
        and by how much
    """
    stock = SHEET.worksheet("stock")
    if pizza_option == "Margherita for Mares":
        print("Margherita here", pizza_option)
    print("Pony", stock.cell(2, 1).value)
    print("stock_checker", pizza_option, quantity, stock.acell("A2"))


def main():
    """Creates a function called main. This function controls the flow of the program"""
    # present Nags with notions welcome & pizza menu
    initial_screen_display()
    pizza_option_user_input_validator()
    
main()
