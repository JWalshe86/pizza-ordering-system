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


class DisplayToUser:
    """
    main class covering information to display to user
    """

    def __init__(self):
        # As I always want this to run first, I'll run this function in the initialiser function
        # which is automatically always called
        self.initial_screen_display()
        self.yes_no_display_to_user()
        self.pizza_options_display_to_user()
        self.pizza_option_number = None

    def initial_screen_display(self):
        """content for initial user interaction with system"""
        print(
            "\033[1m"
            + "Welcome to "
            + colored("Nags with Notions!", "red")
            + "\033[0m\n"
        )
        print("Do you want to order?")
        print("Please answer 'yes' or 'noo'\n")

    def yes_no_display_to_user(self):
        """request a yes no answer from user re proceeding to order"""
        self.user_input_request = input("Enter 'yes' or 'no' here:\n")

    def pizza_options_display_to_user(self):
        """display table with menu options to user"""       
        print(
            tabulate(
                menu_data,
                headers=["Option", "Name", "Price(€)"],
                numalign="center",
                tablefmt="double_outline",
            ),
        )
        self.request_pizza_option_number()

    def request_pizza_option_number(self):
        """request number option from user"""
        print("get pizza no here")
        self.pizza_option_number = input("Enter a number between 1 and 5 here:\n")

DisplayToUser()




# def get_order_request():
#     """Get order request input from the user"""

#     while True:
#         print(
#             "\033[1m"
#             + "Welcome to "
#             + colored("Nags with Notions!", "red")
#             + "\033[0m\n"
#         )
#         print("Do you want to order?")
#         print("Please answer 'yes' or 'no'\n")

#         user_input_yesno_data = input("Enter 'yes' or 'no' here:\n")
#         print(f"You said {user_input_yesno_data}\n\n")

#         # when the validate function returns true this the while loop ends
#         if validate_user_yes_no(user_input_yesno_data):
#             print("Input valid!")
#             break


# def display_menu(data):
#     """
#     displays the menu as per the google sheet menu page
#     """
#     print(
#         tabulate(
#             data,
#             headers=["Option", "Name", "Price(€)"],
#             numalign="center",
#             tablefmt="double_outline",
#         ),
#     )


# class Validation:
#     """
#     main class covering general validation processes
#     initialise important info about validation"""

#     def __init__(self):
#         # validation class attributes
#         self.yes_answer = "yes"
#         self.valid_ans_message = ""
#         print(self.valid_ans_message)
#         # method to validate user input

#     def validate_user(self):
#         """actions to run when user has valid response"""
#         print("validate user")
#         try:
#             if self.yes_answer == "yes":
#                 print("your yes/no answer is valid")
#         except ValueError as e:
#             print(f"Invalid entry: {e}, please try again\n")

    # try:
    #     if self.yes_answer == "yes":
    #         print("Here is our" + "\033[1m" + " pizza menu")
    #         display_menu(menu_data)
    #         pizza_option = input("Enter a number between 1 and 5 here:\n")
    #         validate_get_user_menu_options(pizza_option)
    #     elif input_data == "no":
    #         print("Thats okay, hope to see you again soon")
    #     else:
    #         raise ValueError(f"Number must be between 1 and 5, you said {(input_data)}")
    # except ValueError as e:
    #     print(f"Invalid entry: {e}, please try again\n")
    #     # if an error occurs
    #     return False

    #     # if the function runs without any errors
    # return True
    #     pass


# yes/no option child class of general validation class
# pass validation class in as argument so childclass inherits validation functions
# class ValidateYesNoOption(Validation):
# """to make changes only to the child class"""
# def __init__(self):
# super function gives access to parent Validation values
# super().__init__()
# change valid ans message for pizza option selection
#     valid_ans_message = "Your yes no response is valid"
#     print(valid_ans_message)
# def print_yesno_option_valid_response(self):
#     """actions to run if yes/no option is valid
#     """
#     print("Your yes no response is valid")


# pizza option child class of general validation class
# class ValidatePizzaOption(Validation):
#     """to make changes only to the child class"""
#     def __init__(self):
# super function gives access to parent Validation values
# super().__init__()
# change valid ans message for pizza option selection
#     valid_ans_message = "Your number is valid"
#     print(valid_ans_message)
# def print_pizza_option_valid_response(self):
#     """actions to run if pizza option is valid
#     """
#     print("Your number is valid")


# my_validator = Validation()

# my_validator.validate_user()

# print(f"checking my validation class: {my_validator.user_input_valid}")


# def validate_user_yes_no(input_data):
#     """
#     validate if user inputs yes or no string and if not they are informed they need to do so
#     """

#     try:
#         if input_data == "yes":
#             print("Here is our" + "\033[1m" + " pizza menu")
#             display_menu(menu_data)
#             pizza_option = input("Enter a number between 1 and 5 here:\n")
#             validate_get_user_menu_options(pizza_option)
#         elif input_data == "no":
#             print("Thats okay, hope to see you again soon")
#         else:
#             raise ValueError(f"Number must be between 1 and 5, you said {(input_data)}")
#     except ValueError as e:
#         print(f"Invalid entry: {e}, please try again\n")
#         # if an error occurs
#         return False

#         # if the function runs without any errors
#     return True


# def validate_get_user_menu_options(pizza_option):
#     """_summary_
#     validate if the user input is an integer between 1-5
#     if not the user is informed that they need to re-enter their option

#     """
#     try:
#         if int(pizza_option) >= 1 and int(pizza_option) <= 5:
#             i = pizza_option
#             pizza_names = menu.cell(i, 2).value
#             pizza_price = menu.cell(i, 3).value
#             print(f"You have chosen {pizza_names} at a cost of €{pizza_price}")
#         else:
#             raise ValueError(
#                 f"Exactly yes or no answer required, you said {(pizza_option)}"
#             )
#     except ValueError as e:
#         print(f"Invalid entry: {e}, please try again\n")


# get_order_request()
