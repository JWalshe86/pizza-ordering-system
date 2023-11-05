"""Module used here to clear terminal screen"""
import os
import time
import random
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
MENU = SHEET.worksheet("menu")
# all the order sheet data
MENU_DATA = MENU.get_all_values()

# Active Global Variables
CURRENT_ORDER = []
TOTAL_COST = []
QUANT_PIZZA_HOLDER = []
CART_DISPLAY = []

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
    total_pizza_sum = calc_how_many_pizzas(pizza_name, pizza_quantity)
    current_total = total_cost_calculator(pizza_quantity, pizza_price)
    add_pizza_choice_and_name_to_order_sheet(pizza_name, pizza_price)
    estimated_cooking_time = calculate_estimated_cooking_time(total_pizza_sum)
    shopping_cart(pizza_quantity, pizza_name, current_total)
    finished_order = have_finished_order()
    reference_number = create_order_reference()
    final_message(finished_order, estimated_cooking_time, reference_number)


def initial_screen_display():
    """content for initial user interaction with system
    display table with menu to user"""
    # TODO: find alternative to global variable here
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
    # show logo for 3 seconds then clear screen
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
                    MENU_DATA,
                    headers=["Option", "Name", "Price(€)"],
                    numalign="center",
                    tablefmt="double_outline",
                ),
            )

            pizza_option = int(
                input("Which pizza would you like? Enter number 1 - 5:\n")
            )
            # removes pizza_options and displays how many would you like
            time.sleep(1)
            os.system("cls")

            if 1 <= pizza_option <= 5:
                print("How many would you like?\n")

                break

            raise ValueError
        except ValueError:
            not1_5 = "not a number between 1 and 5"
            not1_5 = colored(not1_5, "red", attrs=["reverse", "blink"])
            print(not1_5)
            time.sleep(3)
    return pizza_option


def quantity_user_input():
    """Check if user has inputted valid data & let them know if they have not
    Args:

    Returns:
        _type_: boolean_description_if no errors returns True
    """
    quant_pizza_check = [len(sub_list) for sub_list in QUANT_PIZZA_HOLDER]
    quant_pizza_check = sum(quant_pizza_check)
    # infinite loop thats only broken if valid input is given
    while True:
        try:
            # code that might crash
            pizza_quantity = input("\033[1m" + "Enter number between 1 and 10 here:\n")
            print(
                "pz q + pz check in userinput", int(pizza_quantity) + quant_pizza_check
            )
            os.system("cls")
            if (
                int(pizza_quantity) >= 0
                and int(pizza_quantity) <= 11
                and int(pizza_quantity) + quant_pizza_check < 10
            ):
                # add the quantity order to the add to sheet function
                add_quantity_to_order_sheet(pizza_quantity)
                break

            # https://stackoverflow.com/questions/7075200/converting-exception-to-a-string-in-python-3
            # pass pizza q to except through exception class
            class PizzaqException(Exception):
                """_summary_class that raises exception and passes pizza quantity as the second argument

                Args:
                    Exception (_type_):string _description_passes pizza quantity as string to except statement
                """

                def __init__(self, pizza_quantity):
                    self.pizza_quantity = pizza_quantity

            # raise Error
            raise PizzaqException(pizza_quantity)
        except PizzaqException as e:
            not1_10 = "Quantity must be a number between 1 and 10\n"
            not1_10 = colored(not1_10, "red", attrs=["reverse", "blink"])
            print(not1_10)
            quantity = str(e)
            quant_pizza_check -= int(quantity)
            # covers if first no. smaller than second
            if quant_pizza_check <= 0:
                quant_pizza_check += int(quantity)

    return pizza_quantity


def have_finished_order():
    """check if user has finished order or wants
    to go back and add more to order

    Returns:
        _type_: _description_
    """
    while True:
        try:
            finish_order = input("\nHave you completed your order? (yes/no):  ")
            print("Please enter 'yes or 'no\n")
            os.system("cls")

            # check for variations of yes/no
            # adapted from https://bobbyhadz.com/blog/python-input-yes-no
            yes_choices = ["yes", "y"]
            no_choices = ["no", "n"]

            # lower() function used in case user inputs capitals
            if finish_order.lower() in yes_choices:
                break
            if finish_order.lower() in no_choices:
                print("You said no")
                main()
                break

            print("Type yes or no")

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
    pizza_name = MENU.cell(i, 2).value
    pizza_price = MENU.cell(i, 3).value
    return pizza_name, pizza_price


def calc_how_many_pizzas(pizza_name, pizza_quantity):
    """_summary_calculate the users total cost as items are
    added to the list. Returns this to main()
    """
    pizza_name_by_quantity = [pizza_name] * int(pizza_quantity)
    QUANT_PIZZA_HOLDER.append(pizza_name_by_quantity)

    total_pizza_sum = [len(sub_list) for sub_list in QUANT_PIZZA_HOLDER]
    total_pizza_sum = sum(total_pizza_sum)
    CURRENT_ORDER.append(pizza_name)
    return total_pizza_sum


def shopping_cart(pizza_quantity, pizza_name, current_total):
    """_summary_presents total order as x: pizza names. Continually
    updates as user selects more pizzas

    Args:
        pizza_name (_type_): _description_string
        pizza_quantity (_type_): _description_string

    Returns:
        _type_: _description_dictionary with brackets removed to show quantity & type of pizza
    """

    total_cost = sum(TOTAL_COST)
    print("                   ---------- YOUR CART ---------\n")

    CART_DISPLAY.append([pizza_quantity, pizza_name, current_total, total_cost])

    print(
        "Quantity               Item                            Price       Overall Price\n"
    )

    while len(CART_DISPLAY[0]) <= 6:
        i = int(len(CART_DISPLAY)) - 1
        for b in range(3, len(CART_DISPLAY[i])):
            CART_DISPLAY[i].insert(b * 1, "           ")
            CART_DISPLAY[i].insert(b * -1, "   ")
        break
    # TODO: find alternative way to display cart here
    [print(*x) for x in CART_DISPLAY]


def create_order_reference():
    """Generate random number between 1- 1000 and set as reference"""
    random_number = random.randint(0, 1000)
    return random_number

    # code inspiration from useriasminna


def calculate_estimated_cooking_time(total_pizza_sum):
    """calculate the estimated cooking time in relation
    to the amount of pizzas ordered. Nags with Notions have
    2 ovens, and each pizza takes 15 mins to cook
    """
    # code adapted from
    # https://stackoverflow.com/questions/69577262/how-to-count-elements-in-nested-lists\nmp/
    estimated_cooking_time = 0

    for i in range(1, 11, 1):
        for j in range(15, 100, 15):
            # for even numbers
            if total_pizza_sum == i and int(i) % 2 == 0:
                estimated_cooking_time = i * j / 2
                break
            # for odd numbers
            if total_pizza_sum == i:
                # margin of error higher at longer cook times of 5+ min
                estimated_cooking_time = (i * j / 2) / 5 + 3
    return estimated_cooking_time


def final_message(finished_order, estimated_cooking_time, reference_number):
    """final message displaying reference number,
    and estimated cooking time. Only runs if finished order is true.
    """
    while finished_order in ("yes", "y"):
        print(
            (
                "\033[1m" + "                      "
                "Thank you for choosing Nags with Notions! Enjoy your meal!"
                + "\033[0m \n"
            )
        )
        print(
            "Quantity               Item                            Price       Overall Price\n"
        )
        [print(*x) for x in CART_DISPLAY]
        print(f"\n\nYour reference number is: PZ{reference_number}")
        print(f"\nEstimated cooking time: {int(estimated_cooking_time)} minutes\n")
        break


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
    return quantity_selection


def total_cost_calculator(quantity: str, pizza_price) -> int:
    """function to calculate total price. Quantity taken from add values function. Quantity argument
    then multiplied with corresponding price in excel sheet.
    Total price then added to total price column in excel

    Args:
        quantity (string): Users selection of amount of pizzas required.
    """
    order = SHEET.worksheet("order")
    i = len(order.col_values(1))
    current_total = int(quantity[0]) * int(pizza_price)
    order.update_cell(i, 4, f"{current_total}")
    TOTAL_COST.append(int(current_total))
    return current_total


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
