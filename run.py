import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pizza_ordering_system_data')

# link to order sheet
order = SHEET.worksheet('order')
# all the order sheet data
data = order.get_all_values()

def get_order_request():
    """Get order request input from the user
    """
    print('Do you want to order?')
    print("Please answer 'yes' or 'no'")
    print('Example: yes')
    
    user_input_data = input("Enter 'yes' or 'no' here:")
    print(f'You said {user_input_data}')
    
get_order_request()