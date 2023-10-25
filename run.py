import os
import time
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from termcolor import colored
from collections import Counter

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
            # present Nags with notions welcome & pizza menu
    initial_screen_display()
    # infinite loop thats only broken if valid input is given
    while True:
        try:
            # code that might crash
            pizza_option = pizza_option_input()
            pizza_name, pizza_price = get_pizza_name_and_price_ordered(pizza_option)
            if int(pizza_option) >= 1 and int(pizza_option) <= 5:
                
                print(f"You have chosen {pizza_name} at a cost of €{pizza_price}\n\n")
                print(f"How many {pizza_name} would you like?\n")
                
                add_pizza_choice_and_name_to_order_sheet(pizza_name, pizza_price)
                    
                pizza_quantity = order_quantity()
                quantity_user_input_validator(pizza_quantity)
                
                currentOrder.append(pizza_name)
                print('current order *', currentOrder)
                
                res = [pizza_name]*int(pizza_quantity)
                print('result1', res)
                
                # res = str(res)[1:-1]
                # res = list(res)
                
            
                print('result', res)
                    
                quant_pizza_holder.append(res)
                print('pizza_quant_holder', quant_pizza_holder)
                
                # how to flatten list from bobbyhadz
                flat_list = [x for xs in quant_pizza_holder for x in xs]
                print('round 1million', flat_list) 
                counter = Counter(flat_list)
                print('this is counter', counter)    
    
            finished_order = have_finished_order()
            if finished_order == 'no':
                    print('finish order no', finished_order)
                    continue
            break
                # break  # exit the immediate loop
                
        except ValueError as e:
            print(f"\nInvalid pizza option entry: {e}, please try again\n")
            print("not a number between 1 and 5")
            


def quantity_user_input_validator(pizza_quantity):
    """Check if user has inputted valid data & let them know if they have not
    Args:
        pizza_quantity (str): _description_ the numerical option the use it's 1-10 for quantity.
        i
    Returns:
        _type_: boolean_description_if no errors returns True
    """
    # passing data in this way adapted from Data Analytics Ireland. 
    # This video was used as a means to get over
    # the issue of wishing to pass data to one function from 2 different functions
    overall_price = total_price(pizza_quantity)

    # infinite loop thats only broken if valid input is given
    while True:
        try:
            
            # code that might crash
            if int(pizza_quantity) >= 1 and int(pizza_quantity) <= 10:
                # add the quantity order to the add to sheet function
                add_quantity_to_order_sheet(pizza_quantity)
                
                print('cur order', currentOrder) 

                print(f'Current order: {pizza_quantity} {currentOrder} at a cost of €{overall_price}')
                pizza_quantity_holder.append(int(pizza_quantity))
                # add the quantities if user goes back to select more pizzas
                totalquantity = sum(pizza_quantity_holder)
                total_cost = sum(currentOrderCost) / 2
                
                print(f'\nYour total order is {totalquantity}: current order at a cost of {int(total_cost)}\n')
                
                break
        except ValueError as e1:
            print(f"\nInvalid quantity entry: {e1}, please try again\n")
            print("Must be a number between 1 and 10")
            main()

def have_finished_order():
    """check if user has finished order or wants
    to go back and add more to order

    Returns:
        _type_: _description_
                    """
    finish_order = input('Have you completed your order?')
                    
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

def initial_screen_display():
    """content for initial user interaction with system
    display table with menu to user"""
    print("\033[1m" + "Welcome to " + colored("Nags with Notions!", "red") + "\033[0m")
    time.sleep(2)
    os.system("cls")
    
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


def main():
    """Creates a function called main. This function controls the flow of the program"""
    
    pizza_option_user_input_validator()


main()
