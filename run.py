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

def initial_screen_display():
    """content for initial user interaction with system"""

    print(
        "\033[1m" + "Welcome to " + colored("Nags with Notions!", "red") + "\033[0m\n"
    )
    print("Do you want to order?")


def yes_no_display_to_user():
    """request a yes no answer from user re proceeding to order
    while loop ensures input request & yes no validator repeated each time loop runs"""

    while RUN_INPUT:
        initial_screen_display()
        user_input_request = input("Enter 'yes' or 'no' here:\n")
        yes_no_display_validator(user_input_request)


def yes_no_display_validator(user_input_request):
    """validate user yes no response"""
    try:
        if user_input_request == "yes":
            print("\n\nHere is our" + "\033[1m" + " pizza menu")
            pizza_options_display_to_user()
            request_pizza_option_number()
            RUN_INPUT = False
            if RUN_INPUT is False:
                exit()
        elif user_input_request == "no":
            print('See you again')
            exit()

        else:
            raise ValueError(
                print(f"Answer must be yes or no, you said {user_input_request}")
            )
    except ValueError as e:
        print(f"\nInvalid entry: {e}, please try again\n")
        # if an error occurs
        return False

    # if the function runs without any errors
    return True
    pass


def request_pizza_option_number():
    """request number option from user"""

    # while True:
    pizza_option_number = input("Enter a number between 1 and 5 here:\n")
    request_pizza_option_validator(pizza_option_number)
        
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
    

def request_pizza_option_validator(data):
    """Check if user has inputted an integer between 1 - 5

    Args:
        data (integer): _description_

    Returns:
        _type_: boolean_description_if no errors returns True
    """
    try:
        if int(data) >= 1 and int(data) <= 5:
            i = data
            pizza_names = menu.cell(i, 2).value
            pizza_price = menu.cell(i, 3).value
            print(f"You have chosen {pizza_names} at a cost of €{pizza_price}")
        else:
            raise ValueError(
                print(f"Answer must be 1 - 5, you said {data}")
            )
    except ValueError as e:
        print(f"\nInvalid entry: {e}, please try again\n")
        request_pizza_option_number()
        return False
        # if an error occurs
        

    # if the function runs without any errors
    return RUN_INPUT is True
    pass

def main():
    """function which I want to run each time"""
    yes_no_display_to_user()


main()
