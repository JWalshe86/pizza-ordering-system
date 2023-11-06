# PIZZA ORDER SYSTEM
  - [OVERVIEW](#overview)
  - [UX/UI](#uxui)
    - [STRATEGY](#strategy)
      - [Goals<br>](#goals)
      - [User Stories<br>](#user-stories)
    - [SCOPE<br>](#scope)
    - [STRUCTURE<br>](#structure)
    - [FLOWCHARTS<br>](#flowcharts)
    - [SURFACE/DESIGN<br>](#surfacedesign)
    - [EXISTING FEATURES<br>](#existing-features)
    - [FUTURE FEATURES<br>](#future-features)
  - [BUGS OR ERRORS](#bugs-or-errors)
  - [TESTING](#testing)
  - [MODULES IMPORTED](#modules-imported)
  - [DEPLOYMENT](#deployment)
    - [CREATING THE WEBSITE](#creating-the-website)
    - [DEPLOYING ON HEROKU](#deploying-on-heroku)
    - [FORK THE REPOSITORY](#fork-the-repository)
    - [CLONE THE REPOSITORY](#clone-the-repository)
  - [CREDITS](#credits)
  - [TOOLS](#tools)
  - [ACKNOWLEDGEMENTS](#acknowledgements)
## OVERVIEW

## UX/UI
### STRATEGY
#### Goals<br>


#### User Stories<br>

### SCOPE<br>

### STRUCTURE<br>
#TODO: need a wireframe

### FLOWCHARTS<br>

### SURFACE/DESIGN<br>

## FEATURES
### EXISTING FEATURES

### FUTURE FEATURES

## Technologies used
- HeroKu - Used to host and deploy website.
- The Tabulate library was used to import tabulate to create the table 
that presents the pizza menu.
- The termcolor library was used to import colored to highlight some text

## BUGS OR ERRORS

![Estimated time not calculated after quantity surpassed](./assets/images/bugs_images/Est_cook_time_error_after_pizza_q_surpass.png)
 
## TESTING

[Pylint Actions 261023](./Pylint_actions261023.pdf)
[Pylint Actions 051123](./testing/pylint_report_051123.txt) Your code has been rated
 at 8.35/10 (previous run: 8.35/10, +0.00)
 * The global statement for 'initial screen display' has run was left in the code, despite being
 highlighted by Pylint. This is because it appears to work well and I don't know another way to prevent the 
 screen display when the user selects they want to add more items to their order. 
 * The code to display the cart items: [print(*x) for x in CART_DISPLAY] has been highlighted by Pylint for not being assigned to a variable. This was temporarily ignored as it's working well and I don't know an alternative. Eventually, thanks to StackOverflow, I found a resolution by using a for loop and " ".join() mapping each item in the nested list to a string with map(). Map was used to manipulate all the items and convert each item to a string which is then joined with " " so each item can be printed on separate lines.
 * After addressing the recommendations the Pylint report reads: Your code has been rated at 9.66/10 (previous run: 9.60/10, +0.06). It's just the above two recommendations to address. 
 * [Code Institute Pylinter 051123](./testing/Code_Institute_Pylinter_051123.pdf)
 * [Code Institute Pylinter cleared](./testing/CI_Pylinter_cleared.png)
 * Test run on Heroku 05/11/23. os.system('cls') not recognised by Heroku but os.system('clear') is. Solved with the following if statement: os.system('cls' if os.name=='nt' else 'clear'). I also had to run pyfiglet to my requirement.txt, so Heroku could recognize it as a dependency.

## MODULES IMPORTED
 * The os module was used for its ability to manipulate the operating system, particularly to clear
 the terminal screen. 
 * The time module was used to complement the os module and delay when items were displayed or 
 lengthen the time an item was displayed.
 * The random module was used to present a random number that could be used for the reference.
 * The Gspread module was used to manipulate Google Sheets.
 * The pyfiglet module was imported to style the Nags with Notions banner. 


## DEPLOYMENT

### CREATING THE WEBSITE
I have used the [Code Institute Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template) to create a terminal where my Python code will generate its output.

  
### DEPLOYING ON HEROKU
- Install Gspread using pip install Gspread in the terminal
- Ensure the requirement.txt file in the virtual working environment contains Gspread
- Enter [Heroku](https://id.heroku.com/login) and click 'Create new App'.
- Store sensitive data contained in the creds.json file in the config/Environment Vars
- Add both Python and node.js buildpacksClick Deploy and then connect to GitHub
- Search and connect to the GitHub repository name
- Click deploy branch
- When the project has been successfully deployed, click view.

### FORK THE REPOSITORY 


### CLONE THE REPOSITORY


## CREDITS
* Readme template adapted from [useriasminna](https://github.com/useriasminna/american_pizza_order_system/blob/main/README.md)
* Inspiration for the large title heading from [LauraMaynock]
* Manipulating Google Sheets [Gspread](https://docs.Gspread.org/en/latest/user-guide.html)](https://docs.Gspread.org/en/latest/user-guide.html)
* Try catch with loop [Paul Miskew](https://youtu.be/b0q9vVgAMq8?si=U_UnqDxHyZegVnsX)
* [How to pass data between functions](https://www.youtube.com/watch?v=GsKDtSHRHdI) this video was used as a means to get over the issue of wishing to pass data to one function from 2 different functions
* [Print two lists side by side on Stackoverflow ](https://stackoverflow.com/questions/48053979/print-2-lists-side-by-side)
* [How to flatten a list from bobbyhadz blog](https://bobbyhadz.com/blog/python-remove-square-brackets-from-list)
* [Switching keys and values in a dictionary from Stackoverflow](https://stackoverflow.com/questions/8305518/switching-keys-and-values-in-a-dictionary-in-python)

## TOOLS
[GitHub](https://GitHub.com/) - used for hosting the source code of the program
[Google Drive API](https://developers.google.com/drive/api)- to develop apps that integrate with Drive
[Google Sheets API](https://developers.google.com/sheets/api/guides/concepts) - to read and modify Google Sheets data
[Google Auth](https://developers.google.com/identity/protocols/oauth2) - allows access to Google APIs
[Gspread](https://docs.Gspread.org/en/v5.10.0/) - Python API for Google Sheets [Lucid Chart](https://www.lucidchart.com/pages/landing?utm_source=google&utm_medium=cpc&utm_campaign=_chart_en_tier1_mixed_search_brand_exact_&km_CPC_CampaignId=1490375427&km_CPC_AdGroupID=55688909257&km_CPC_Keyword=lucid%20chart&km_CPC_MatchType=e&km_CPC_ExtensionID=&km_CPC_Network=g&km_CPC_AdPosition=&km_CPC_Creative=442433236001&km_CPC_TargetID=kwd-55720648523&km_CPC_Country=1007872&km_CPC_Device=c&km_CPC_placement=&km_CPC_target=&gad_source=1&gclid=Cj0KCQjwj5mpBhDJARIsAOVjBdpyfLPu38m7pDBye0tpLWTp5UQgTyONWR-mthQQ3mR1Iy3LiHHuXm4aArNSEALw_wcB)](https://www.lucidchart.com/pages/landing?utm_source=google&utm_medium=cpc&utm_campaign=_chart_en_tier1_mixed_search_brand_exact_&km_CPC_CampaignId=1490375427&km_CPC_AdGroupID=55688909257&km_CPC_Keyword=lucid%20chart&km_CPC_MatchType=e&km_CPC_ExtensionID=&km_CPC_Network=g&km_CPC_AdPosition=&km_CPC_Creative=442433236001&km_CPC_TargetID=kwd-55720648523&km_CPC_Country=1007872&km_CPC_Device=c&km_CPC_placement=&km_CPC_target=&gad_source=1&gclid=Cj0KCQjwj5mpBhDJARIsAOVjBdpyfLPu38m7pDBye0tpLWTp5UQgTyONWR-mthQQ3mR1Iy3LiHHuXm4aArNSEALw_wcB) - to create flow chart outlining the project.

## ACKNOWLEDGEMENTS
