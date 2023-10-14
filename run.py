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


def initial_screen_display():
    """content for initial user interaction with system"""
    print(
        "\033[1m" + "Welcome to " + colored("Nags with Notions!", "red") + "\033[0m\n"
    )
    print("Do you want to order?")
    print("Please answer 'yes' or 'no'\n")


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
    request_pizza_option_number()

def yes_no_display_to_user():
    """request a yes no answer from user re proceeding to order"""
    while True:
        user_input_request = input("Enter 'yes' or 'no' here:\n")
        return user_input_request
        

def yes_no_display_validator(data):
    """validate usesr yes no response"""
    try:
        if data == "yes":
            print("Here is our" + "\033[1m" + " pizza menu")
            pizza_options_display_to_user()
        elif data == "no":
            exit()
        else:
            raise ValueError(
                f"Answer must be yes or no, you said {data}"
            )
    except ValueError as e:
        print(f"\nInvalid entry: {e}, please try again\n")
        # if an error occurs
        return False

    # if the function runs without any errors
    return True
    pass

user_input = yes_no_display_to_user()
yes_no_display_validator(user_input)


def request_pizza_option_number():
    """request number option from user"""
    pizza_option_number = input("Enter a number between 1 and 5 here:\n")

    try:
        if int(pizza_option_number) >= 1 and int(pizza_option_number) <= 5:
            i = pizza_option_number
            pizza_names = menu.cell(i, 2).value
            pizza_price = menu.cell(i, 3).value
            print(f"You have chosen {pizza_names} at a cost of €{pizza_price}")
        else:
            raise ValueError(
                f"Number must be between 1 and 5, you said {(pizza_option_number)}"
            )
    except ValueError as e:
        print(f"Invalid entry: {e}, please try again\n")
        # if an error occurs
        return False

        # if the function runs without any errors
    return True
    pass


def main():
    """function which I want to run each time"""
    initial_screen_display()
    yes_no_display_to_user()


main()
