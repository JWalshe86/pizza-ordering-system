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
totalCost = []
quant_pizza_holder = []
cart_display = []

INITIAL_SCREEN_DISPLAY_HAS_RUN = False

def main():
    """Creates a function called main. This function controls the flow of the program
    Also has the benefit of having returned values in the same place and these can contribute
    to other, more complex functions, as the project progresses"""
    # present Nags with notions welcome & pizza menu
    initial_screen_display()
    pizza_option = pizza_option_input()
    pizza_quantity = quantity_user_input()
    pizza_name, pizza_price = get_pizza_name_and_price_ordered(pizza_option)
    calc_overall_cost(pizza_name, pizza_quantity)
    total_cost = total_cost_calculator(pizza_quantity, pizza_price)
    add_pizza_choice_and_name_to_order_sheet(pizza_name, pizza_price)
    shopping_cart(pizza_quantity, pizza_name, pizza_price, total_cost)
    finished_order = have_finished_order()

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

def pizza_option_input():
    """create a function to get users pizza choice, return it to the calling function
    which is called in main()
    """
    # infinite loop thats only broken if valid input is given
    while True:
        try:
            # code that might crash
            print("\nPlease select one of the 5 number options below")

            print(
                tabulate(
                    menu_data,
                    headers=["Option", "Name", "Price(€)"],
                    numalign="center",
                    tablefmt="double_outline",
                ),
            )            
            
            
            pizza_option = int(input("Enter a number between 1 and 5 here:\n"))

            time.sleep(1)
            os.system("cls")

            if pizza_option >= 1 and pizza_option <= 5:
                
                print(f"How many would you like?\n")

                break

            else:
                raise ValueError      
        except ValueError:
            not1_5 = "not a number between 1 and 5"
            not1_5 = colored(not1_5, "red", attrs=["reverse", "blink"])
            print(not1_5)
    return pizza_option
            
def quantity_user_input():
    """Check if user has inputted valid data & let them know if they have not
    Args:

    Returns:
        _type_: boolean_description_if no errors returns True
    """

    # infinite loop thats only broken if valid input is given
    while True:
        try:
            # code that might crash
            pizza_quantity = input(
                "\033[1m" + "Enter a number between 1 and 10 here:\n"
            )
            os.system("cls")
            if int(pizza_quantity) >= 1 and int(pizza_quantity) <= 10:
                # add the quantity order to the add to sheet function
                add_quantity_to_order_sheet(pizza_quantity)

                break
            
            raise ValueError
        except ValueError:
            not1_10 = "Must be a number between 1 and 10\n"
            not1_10 = colored(not1_10, "red", attrs=["reverse", "blink"])
            print(not1_10)
        
    return pizza_quantity

def have_finished_order():
    """check if user has finished order or wants
    to go back and add more to order

    Returns:
        _type_: _description_
    """
    while True:
        try:
            finish_order = input("Have you completed your order?")
            print("Please enter 'yes or 'no\n")
            os.system("cls")
            if finish_order == 'yes':
                print('You said yes')
                break
            if finish_order == 'no':
                main()
                break
            
            raise ValueError
        except ValueError:
            notyes_no = "Answer must be yes or no"
            notyes_no = colored(notyes_no, "red", attrs=["reverse", "blink"])
            print(notyes_no)

    return finish_order

def get_pizza_name_and_price_ordered(pizza_option):
    """_summary_

    Returns:
        : _description_a string of the name of the pizza chosen by the user.
        Passes these values back to where they were called in the main function
    """
    i = pizza_option
    pizza_name = menu.cell(i, 2).value
    pizza_price = menu.cell(i, 3).value
    print('pizza price in get pizza price', pizza_price)
    return pizza_name, pizza_price

def calc_overall_cost(pizza_name, pizza_quantity):
    """_summary_calculate the users total cost as items are
    added to the list. Returns this to main()
    """
    pizza_name_by_quantity = [pizza_name] * int(pizza_quantity)
    quant_pizza_holder.append(pizza_name_by_quantity)
    currentOrder.append(pizza_name)

def shopping_cart(pizza_quantity, pizza_name, pizza_price, total_cost):
    """_summary_presents total order as x: pizza names. Continually
    updates as user selects more pizzas

    Args:
        pizza_name (_type_): _description_string
        pizza_quantity (_type_): _description_string

    Returns:
        _type_: _description_dictionary with brackets removed to show quantity & type of pizza
    """
    
    total_cost = sum(totalCost)
    print('     ---------- YOUR CART ---------\n')
    
    cart_display.append([pizza_quantity,pizza_name,pizza_price,total_cost])
    
    # code adapted from stackoverflow 'print a nested list line by line'
    [print(*a)                           #1 Expression
    for a in cart_display][1:-1]        #2 Iteration

    
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
    return  quantity_selection

def total_cost_calculator(quantity: str, pizza_price) -> int:
    """function to calculate total price. Quantity taken from add values function. Quantity argument
    then multiplied with corresponding price in excel sheet.
    Total price then added to total price column in excel

    Args:
        quantity (string): Users selection of amount of pizzas required.
    """
    order = SHEET.worksheet("order")
    i = len(order.col_values(1))
    total = int(quantity[0]) * int(pizza_price)
    print('total cost in cost calc', total, quantity[0], pizza_price)
    order.update_cell(i, 4, f"{total}")
    totalCost.append(int(total))
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
