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


def user_input_validator(data, input_identity):
    """Check if user has inputted valid data & let them know if they have not
    Args:
        data (integer): _description_ the numerical option the user takes whether it's 1-5 
        for pizza or 1-10 for quantity.
        input_identity (string) _description_ returns a value so the validator knows if it's validating
        user input for pizza selection or user input for quantity selection

    Returns:
        _type_: boolean_description_if no errors returns True
    """
    while RUN_INPUT is True:
        
        try:
            if input_identity == 'pizza_option' and int(data) >= 1 and int(data) <= 5:
                i = data
                pizza_names = menu.cell(i, 2).value
                pizza_price = menu.cell(i, 3).value
                print(f"You have chosen {pizza_names} at a cost of €{pizza_price}")
                add_to_order_sheet(pizza_names, pizza_price)
                user_order_quantity_request()
                # adds order to order worksheet
                
            
            elif input_identity == 'order_quantity' and int(data) >= 1 and int(data) <= 10:
                # add the quantity order to teh add to sheet function
                add_to_order_sheet(data)
                print(f'you chose: {data}')
                exit()

            else:
                raise ValueError(print(f"Answer must be 1 - 5, you said {data}"))
        except ValueError as e:
            if input_identity == 'pizza_option':
                print(f"\nInvalid pizza option entry: {e}, please try again\n")
                request_pizza_option_number()
        
            elif input_identity == 'order_quantity':
                print(f"\nInvalid quantity entry: {e}, please try again\n")
            
        # if an error occurs
                return False
    # if the function runs without any errors
    return RUN_INPUT is True
    pass

def add_to_order_sheet(*data):
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
            data = list(data)
            order.update_cell(i,1,f'{data[0]}')
            order.update_cell(i,2,f'{data[1]}')
            break
            
        if len(data[0]) <= 2:
            # iterator already updated by 1 above so no need for +1 here
            i = len(order.col_values(1))
            quantity_selection = list(item)
            order.update_cell(i,3,f'{quantity_selection[0]}')
            break

def initial_screen_display():
    """content for initial user interaction with system"""

    print(
        "\033[1m" + "Welcome to " + colored("Nags with Notions!", "red") + "\033[0m\n"
    )
    print("\n\nPlease select one of the 5 number options below")
    
    pizza_options_display_to_user()

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

def request_pizza_option_number():
    """request number option from user"""

    pizza_option_number = input("Enter a number between 1 and 5 here:\n")
    user_input_validator(pizza_option_number, 'pizza_option')

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
        user_input_validator(order_quantity, 'order_quantity')
        add_to_order_sheet(order_quantity)
        
        
def main():
    """functions which I wish to run everytime"""

    initial_screen_display()


main()