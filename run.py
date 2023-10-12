import gspread
from google.oauth2.service_account import Credentials
import pprint

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


def get_order_request():
    """Get order request input from the user"""
    print("Do you want to order?")
    print("Please answer 'yes' or 'no'")
    print("Example: yes")

    user_input_data = input("Enter 'yes' or 'no' here:\n")
    print(f"You said {user_input_data}")
    validate_user_input_data(user_input_data)


def display_menu():
    """
    displays the menu as per the google sheet menu page
    """
    for new_menu in menu_data:
        print(new_menu, end=",")


def validate_user_input_data(input_data):
    """
    validate if user has inputted yes or no string and if not they are informed they need to do so
    """

    try:
        if input_data == "yes":
            print("Great, lets proceed to the menu")
            display_menu()
        elif input_data == "no":
            print("Thats okay, hope to see you again soon")
        else:
            raise ValueError(
                f"Exactly yes or no answer required, you said {(input_data)}"
            )
    except ValueError as e:
        print(f"Invalid entry: {e}, please try again\n")


get_order_request()
