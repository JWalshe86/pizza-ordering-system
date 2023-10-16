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

RUN_INPUT = True


def user_input_validator(data):
    """Check if user has inputted an integer between 1 - 5

    Args:
        data (integer): _description_

    Returns:
        _type_: boolean_description_if no errors returns True
    """
    
    try:
        if int(data) >= 1 and int(data) <= 5:
            pizza_option_number = input("Enter a number between 1 and 5 here:\n")
            i = pizza_option_number
            pizza_names = menu.cell(i, 2).value
            pizza_price = menu.cell(i, 3).value
            print(f"\n\nYou have chosen {pizza_names} at a cost of €{pizza_price}")
            user_order_quantity_request()
            order = SHEET.worksheet("order")
            # adds order to order worksheet
            order.append_row([f"{pizza_names}", f"{pizza_price}"])
        else:
            raise ValueError(print(f"Answer must be 1 - 5, you said {data}"))
    except ValueError as e:
        print(f"\nInvalid entry: {e}, please try again\n")
        user_input_validator(data)
        return False
        # if an error occurs

    # if the function runs without any errors
    return RUN_INPUT is True
    pass


def initial_screen_display():
    """content for initial user interaction with system"""

    print(
        "\033[1m" + "Welcome to " + colored("Nags with Notions!", "red") + "\033[0m\n"
    )
    print(
        "Please select one of the 5 number options below"
    )
    pizza_options_display_to_user()
    user_input_validator()
    
    
def pizza_options_display_to_user():
    """display table with menu options to user"""
    print(
        tabulate(
            menu_data,
            headers=["Option", "Name", "Price(€)"],
            numalign="center",
            tablefmt="double_outline",
        ),
    )

def user_order_quantity_request():
    """function to get the amount of product the user has ordered
    String argument pizza_names passed so user can chose the quantity of the 
    specific pizza they ordered. 
    """    
    print("\n\n\033[1m" + "Please insert the amount of you want, " +
        "10 pizzas maximum" + "\033[0m \n")
    
    while True:
        print("Enter a number between 1 and 10")
        
        order_quantity = input("\033[1m" + "Write your answer here and"
                        " press Enter when you're ready:\n")
        print('order quantity:', order_quantity)
        
def main():
    """functions which I wish to run everytime"""

    initial_screen_display()

main()
