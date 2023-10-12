import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

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

    user_input_yesno_data = input("Enter 'yes' or 'no' here:\n")
    print(f"You said {user_input_yesno_data}")
    validate_user_yes_no(user_input_yesno_data)

def display_menu(data):
    """
    displays the menu as per the google sheet menu page
    """
    print(tabulate(data, headers=["Option", "Name", "Price(€)"], numalign="center", tablefmt="double_outline"),)

def validate_user_yes_no(input_data):
    """
    validate if user has inputted yes or no string and if not they are informed they need to do so
    """

    try:
        if input_data == "yes":
            print("Great! here's the menu...\n\n")
            display_menu(menu_data)
            pizza_option = input("Enter a number between 1 and 5 here:\n")
            get_user_menu_options(pizza_option)
        elif input_data == "no":
            print("Thats okay, hope to see you again soon")
        else:
            raise ValueError(
                f"Exactly yes or no answer required, you said {(input_data)}"
            )
    except ValueError as e:
        print(f"Invalid entry: {e}, please try again\n")
        
def get_user_menu_options(pizza_option):
    """return the options the user chose and add to worksheet named 'order'
    """
    i = pizza_option
    pizza_names = menu.cell(i,2).value
    
    pizza_price = menu.cell(i,3).value
    print(f'You have chosen {pizza_names} at a cost of €{pizza_price}')

get_order_request()
