# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2.0},
    "Super Mario Bros": {"quantity": 5, "cost": 3.0},
    "Tetris": {"quantity": 2, "cost": 1.0},
    # Add more games as needed
}

# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function to display available games with their numbers and rental costs
def display_available_games():
    print("Available Games: \n")

    if game_library["Donkey Kong"]["quantity"] != 0:
        print("Donkey Kong: ", game_library["Donkey Kong"]["quantity"], "copies, ", "rental cost: $", game_library["Donkey Kong"]["cost"], "\n")

    if game_library["Super Mario Bros"]["quantity"] !=0:
        print("Super Mario Bros: ", game_library["Super Mario Bros"]["quantity"], "copies, ", "rental cost: $", game_library["Super Mario Bros"]["cost"], "\n")

    if game_library["Tetris"]["quantity"] != 0:
        print("Tetris: ", game_library["Tetris"]["quantity"], "copies, ", "rental cost: $", game_library["Tetris"]["cost"], "\n")
    else:
        print("Currently no games available.\n")
    
# Function to register a new user
def register_user(username, password, free_rental = 0,  transactions = 0, balance = 0.0, points = 0.0, inventory =[]):
    balance = float(balance)
    points = float(points)
    free_rental = float(free_rental)
    account = {"username" : username, "password": password, "free rental": free_rental, "transactions": transactions, "balance": balance, "points": points, "inventory": inventory}
    user_accounts[username] = account

# Function to rent a game
def rent_game(username):
    display_available_games()
    balance = user_accounts.get(username, {}).get("balance")
    print(f"Your balance: {balance}")
    rent_choice = int(input("What will you use? (1 for Free Rentals, 0 for Money): "))
    
    choice = input("Pick a game you want to rent: ")

    if choice not in game_library:
        print("Game not found.")
        logged_in_menu(username)
    
    game = game_library[choice]
    if game["quantity"] == 0:
        print(choice, " has no more copies left.")
        logged_in_menu(username)
    
    if rent_choice == 0:
        if user_accounts[username]["balance"] < game["cost"]:
            print("Not enough balance.")
            logged_in_menu(username)
        
        else:
            user_accounts[username]["balance"] -= game["cost"]
            user_accounts[username]["transactions"] += game["cost"]
            user_accounts[username]["inventory"].append(choice)
            game["quantity"] -= 1
            print("You have rented ", choice)
            logged_in_menu(username)
        
    elif rent_choice == 1:
        free_rental = user_accounts.get(username, {}).get("free_rental")
        if free_rental == 0:
            print("You have no points.")
        else:
            user_accounts[username]["free_rental"] -= 1
            user_accounts[username]["inventory"].append(choice)
            game["quantity"] -= 1
            print("You have rented ", choice)
    
# Function to return a game
def return_game(username):
    print("Inventory: ")
    for inventory_games in user_accounts[username]["inventory"]:
        print(inventory_games)

    choice = input("What would you like to return?: ")
    if choice in user_accounts[username]["inventory"]:
        if game_library[choice]["quantity"] != 0:
            game_library[choice]["quantity"] += 1
            user_accounts[username]["inventory"].remove(choice)
            print(f"You have returned {choice}.")
            logged_in_menu(username)
    else:
        print("Game not found in your inventory.")
        logged_in_menu(username)

# Function to top-up user account
def top_up_account(username, amount):
    if amount > 0:
        user_accounts[username]["balance"] += amount
        print("Account successfully topped up.")
        logged_in_menu(username)
    else:
        print("Negative numbers are invalid")
        logged_in_menu(username)

# Function to display user's inventory
def display_inventory(username):
    inventory = user_accounts[username]["inventory"]
    if inventory:
        print("Your inventory:")
        for rental in inventory:
            print(rental)
        logged_in_menu(username)
    else:
        print("Your inventory is empty.")
    logged_in_menu(username)

# Function for admin to update game details
def admin_update_game():
    while True:
        display_available_games()
        print("""
            1. Price
            2. Copies
            3. Exit
            """)
        try:
            choice = int(input("What would you like to edit?: "))
            if choice == 1:
                game_name = input("\nWhich game would you like to edit the price of?: ")
                if game_name in game_library:
                    try:
                        new_cost = float(input("\nHow much would it cost now?: $"))
                        if new_cost > 0:
                            game_library[game_name]["cost"] = new_cost
                            print("Update Successful!")
                        elif new_cost == 0:
                            print("Please input a number greater than 0.")
                        else:
                            print("Please input a positive number.")
                    except ValueError:
                        print("Please input a number.")
                else:
                    print("Game not found.")

            elif choice == 2:
                game_name = input("Which game would you like to edit the copies of?: ")
                if game_name in game_library:
                    try:
                        new_copy = int(input("How many copies are there now?: "))
                        if new_copy >= 0:
                            game_library[game_name]["quantity"] = new_copy
                            print("Update Successful!")
                        else:
                            print("Please input a positive number.")
                    except ValueError:
                        print("Please input a number.")
                else:
                    print("Game not found.")
            
            elif choice == 3:
                admin_menu()
            
            else:
                print("Input a number between 1 and 3.")

        except ValueError:
            print("Please input a number.")

# Function for admin login
def admin_login():
    while True:
        print("Admin Login")
        username = input("\nAdmin username: ")
        if username == admin_username:
            password = input("\nPassword: ")
            if password == admin_password:
                admin_menu()
                break
            else:
                print("\nIncorrect Password\n")
        else:
            print("\nIncorrect username.\n")
        
# Admin menu
def admin_menu():
    while True:
        print("""
              Admin Menu
             1. Update Game Information
             2. Exit
              """)
        try:
            choice = int(input("\nWhat would you like to do?: "))
            if choice == 1:
                admin_update_game()
                break
            elif choice == 2:
                    main()
                    break
            else:
                print("\nPlease enter 1 or 2.")
        except ValueError:
            print("\nPlease input a number.")

# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    user_accounts[username]["points"] = user_accounts[username]["transactions"] / 2
    points = user_accounts[username]["points"]
    rentals = user_accounts[username]["free rental"]

    print("Your points: ", user_accounts[username]["points"], "\n")
    print("2 points = 1 free rental")

    amount = int(input("How many would you like to redeem?: "))
    try:
        if amount > points / 3:
            print("Not enough points.")
            logged_in_menu(username)
        elif amount < 0:
            print("Input a positive number.")
            logged_in_menu(username)
        elif amount >= 1:
            points -= amount * 3
            print("Successfully redeemed ", amount, " free rental(s).")
            rentals += amount
            logged_in_menu(username)
        else:
            logged_in_menu(username)
    except ValueError:
        print("\nPlease input a number.")
        logged_in_menu(username)

# Function to display game inventory
def display_game_inventory():
    print("Game Inventory")
    for game in game_library:
        print(game)

# Function to handle user's logged-in menu
def logged_in_menu(username):
    while True:
        print("""
            User Menu
            
            1. Rent Games
            2. Return Games
            3. View Inventory
            4. Topup
            5. Redeem Free Rental
            6. Exit
            
            """)
        try:
            choice = int(input("What would you like to do?: "))
            if choice == 1:
                rent_game(username)
                break
            elif choice == 2:
                return_game(username)
                break
            elif choice == 3:
                display_inventory(username)
                break
            elif choice == 4:
                account = input("Which account would you like to top up?: ")
                if account in user_accounts:
                    try:
                        amount = float(input("How much would you like to top up?: "))
                        top_up_account(account, amount)
                        logged_in_menu(username)
                    except ValueError:
                        print("Please input a valid number.")
                        logged_in_menu(username)
                else:
                    print("Account not found.")
                logged_in_menu(username)
            elif choice == 5:
                redeem_free_rental(username)
            elif choice == 6:
                main()
                break
            else:
                print("Input a number between 1 and 4.")
                continue
        except ValueError:
                print("Please input a number.")
                continue

# User Login Menu
def check_credentials():
    while True:
        print("Login")
        username = input("Username: ")
        if username in user_accounts:
            password = input("Password: ")
            if password == user_accounts[username]["password"]:
                logged_in_menu(username)
                break
            else:
                print("Incorrect Password")
        elif username == "":
            main()
        else:
            print("Incorrect username.")
    
# Main function to run the program
def main():
    while True:
        print("""
            Main Menu
          
            1. Register
            2. Login
            3. Admin Login
              
            """)
        try:
            choice = int(input("What would you like to do?: "))
            if choice == 1:
                username = input("Enter username: ")
                if username in user_accounts:
                    print("Username already taken.")
                elif username == "":
                    main()
                else:
                    password = input("Enter password: ")
                    if password == "":
                        main()
                    else:
                        register_user(username, password)
                        logged_in_menu(username)
            elif choice == 2:
                check_credentials()  
            elif choice == 3:
                admin_login()
            else:
                print("Input a number between 1 and 3.")
        except ValueError:
            print("Please input a number.")

if __name__ == "__main__":
    main()