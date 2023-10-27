
"""Module used here to clear terminal screen"""
import os
import time
from collections import Counter
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from termcolor import colored
import pyfiglet


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

currentOrder = []
currentOrderCost = []
pizza_quantity_holder = []
quant_pizza_holder = []

INITIAL_SCREEN_DISPLAY_HAS_RUN = False

# FINISHED_ORDER_BOOLEAN = True


def main():
    """Creates a function called main. This function controls the flow of the program"""
    # present Nags with notions welcome & pizza menu
    initial_screen_display()
    pizza_option = pizza_option_input()

# # creates infinite loop which only ends if user says they've finished their order
# while FINISHED_ORDER_BOOLEAN is True:
    pizza_option_user_input_validator(pizza_option)
    finished_order = have_finished_order()

    # if finished_order == "no":
        # FINISHED_ORDER_BOOLEAN = True
        
def initial_screen_display():
    """content for initial user interaction with system
    display table with menu to user"""
    global INITIAL_SCREEN_DISPLAY_HAS_RUN
    # code adapted from bobbyhadz.com so initial screen display only ever runs once
    # and does not re-run when user selects no to finished order
    # as long as its true it returns before inner codes executed,
    # when it's executed it turns true from false,
    # so it's only false the first time
    if INITIAL_SCREEN_DISPLAY_HAS_RUN:
        return
    INITIAL_SCREEN_DISPLAY_HAS_RUN = True

    nags_banner = pyfiglet.figlet_format("Nags with Notions")
    nags_banner = colored(nags_banner, "magenta", attrs=["reverse", "blink"])
    print(nags_banner)
    time.sleep(3)
    os.system("cls")

def pizza_option_user_input_validator(pizza_option):
    """Check if user has inputted valid data & let them know if they have not
    Args:
        data (str): _description_ the numerical option the user takes whether it's 1-5
        for pizza or 1-10 for quantity.
        input_identity (string) _description_ returns
        a value so the validator knows if it's validating
        user input for pizza selection or user input for quantity selection

    Returns:
        _type_: boolean_description_if no errors returns True
    """
    # infinite loop thats only broken if valid input is given
    while True:
        try:
            # code that might crash
            pizza_name, pizza_price = get_pizza_name_and_price_ordered(pizza_option)
            if int(pizza_option) >= 1 and int(pizza_option) <= 5:
                print(f"You have chosen {pizza_name} at a cost of €{pizza_price}\n\n")
                print(f"How many {pizza_name} would you like?\n")

                add_pizza_choice_and_name_to_order_sheet(pizza_name, pizza_price)
                
                pizza_quantity = quantity_user_input_validator()
                
                overall_price = total_price(pizza_quantity)
                currentOrder.append(pizza_name)
                print(
                    f'''\nCurrent selection: {pizza_quantity} {currentOrder[0]},
                    at a cost of €{overall_price}\n'''
                )
                # continually update order as user adds to it
                counter, total_cost = calculate_total_order(pizza_name, pizza_quantity)

                print(f"Total order: {counter} at a cost of €{int(total_cost)}\n")

                break  # exit the immediate loop
    
        except ValueError as e:
            print(f"\nInvalid pizza option entry: {e}, please try again\n")
            print("not a number between 1 and 5")
            continue
    return pizza_name, pizza_quantity

def calculate_total_order(pizza_name, pizza_quantity):
    """_summary_presents total order as x: pizza names. Continually
    updates as user selects more pizzas

    Args:
        pizza_name (_type_): _description_string
        pizza_quantity (_type_): _description_string

    Returns:
        _type_: _description_dictionary with brackets removed to show quantity & type of pizza
    """
    res = [pizza_name] * int(pizza_quantity)

    quant_pizza_holder.append(res)

    # how to flatten list from bobbyhadz
    flat_list = [x for xs in quant_pizza_holder for x in xs]
    total_cost = sum(currentOrderCost) / 2
    counter = Counter(flat_list)

    counter = dict(counter)

    # swap keys and values in dictionary from stackoverflow see credits
    counter = {counter[k]: k for k in counter}
    # remove brackets
    counter = str(counter)[1:-1]

    counter = counter.replace("'", "")    

    return counter, total_cost

def quantity_user_input_validator():
    """Check if user has inputted valid data & let them know if they have not
    Args:
        
    Returns:
        _type_: boolean_description_if no errors returns True
    """
    CORRECT_QUANTITY_INPUT = True
    
    # infinite loop thats only broken if valid input is given
    while CORRECT_QUANTITY_INPUT is True:
        pizza_quantity = input("\033[1m" + "Enter a number between 1 and 10 here:\n")
    
        try:
            # code that might crash

            if int(pizza_quantity) >= 1 and int(pizza_quantity) <= 10:
                # add the quantity order to the add to sheet function
                add_quantity_to_order_sheet(pizza_quantity)

                pizza_quantity_holder.append(int(pizza_quantity))

                break
            
        except ValueError as e1:
            print(f"\nInvalid quantity entry: {e1}, please try again\n")
            print("Must be a number between 1 and 10")
            CORRECT_QUANTITY_INPUT = True
    return pizza_quantity

def have_finished_order():
    """check if user has finished order or wants
    to go back and add more to order

    Returns:
        _type_: _description_
    """
    finish_order = input("Have you completed your order?")
    os.system("cls")

    return finish_order


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


def add_pizza_choice_and_name_to_order_sheet(pizza_name, pizza_price):
    """
    Pizza info taken from pizza validator function. Uploaded to google sheets
    stock sheet here.
    """
    order = SHEET.worksheet("order")

    # iterator is length of columns + 1 so new row entered each time
    i = len(order.col_values(1)) + 1
    order.update_cell(i, 1, f"{pizza_name}")
    order.update_cell(i, 2, f"{pizza_price}")


def add_quantity_to_order_sheet(pizza_quantity):
    """
    Pizza info taken from pizza validator function. Uploaded to google sheets
    stock sheet here.
    """
    order = SHEET.worksheet("order")

    # iterator is length of columns + 1 so new row entered each time
    i = len(order.col_values(1))
    quantity_selection = list(pizza_quantity)
    order.update_cell(i, 3, f"{quantity_selection[0]}")
    total_price(quantity_selection[0])

def pizza_option_input() -> str:
    """create a function to get users pizza choice, return it to the calling function
    which is called in main()
    """
    print("\nPlease select one of the 5 number options below")

    print(
        tabulate(
            menu_data,
            headers=["Option", "Name", "Price(€)"],
            numalign="center",
            tablefmt="double_outline",
        ),
    )
    pizza_option_number = input("Enter a number between 1 and 5 here:\n")
    time.sleep(1)
    os.system("cls")

    return pizza_option_number


def get_pizza_order_quantity():
    """create a function to get users quantity choice, return it to the calling function
    which is called in main()
    """
    


def total_price(quantity: str) -> int:
    """function to calculate total price. Quantity taken from add values function. Quantity argument
    then multiplied with corresponding price in excel sheet.
    Total price then added to total price column in excel

    Args:
        quantity (string): Users selection of amount of pizzas required.
    """
    order = SHEET.worksheet("order")
    i = len(order.col_values(1))
    price = order.cell(i, 2).value
    total = int(quantity) * int(price)
    order.update_cell(i, 4, f"{total}")
    currentOrderCost.append(int(total))
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

main()