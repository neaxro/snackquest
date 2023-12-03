import yaml, sys, argparse
import beeprint as bprint
from models.snack import Snack
from models.order import Order

# Set the argument flags
parser = argparse.ArgumentParser(
    prog="Vending Machine Loot Calculator",
    description="From the given balance and menu list calculates the optimal order to leave as less money on the card as possible."
)
parser.add_argument("balance", help="The current balance of the card [default JMF]", type=int)
parser.add_argument("menu", help="Vending machine's menu [.yml, .yaml]", type=argparse.FileType("r"))
parser.add_argument("-p", "--printMenu", dest="printMenu", action="store_true", help="Prints the menu")
args = parser.parse_args()

# Calculates the best order
def calcOrder(balance: int, snacks: list[Snack]):
    selected_items: list[Order] = []
    
    for snack in snacks:
        if snack.desired > 0:
            balance -= snack.price * snack.desired
            snack.tobuy = snack.desired
            selected_items.append(
                Order(
                    snack.price,
                    snack.desired,
                    snack.name
                )
            )

        snack.desired = 0
    
    if balance <= 0:
        print("Your balance fall below 0 JMF, too much desired snacks!")
        sys.exit(1)
    
    # Smart algorithm
    n = len(snacks)
    prices = [snack.price for snack in snacks]
    prices.sort()
    
    # Init table
    dp = [[0] * (balance + 1) for _ in range(n + 1)]

    # Dinamic programming
    for i in range(1, n + 1):
        for j in range(balance + 1):
            max_value_without_current = dp[i - 1][j]

            for k in range(1, (j // prices[i - 1]) + 1):
                max_value_with_current = dp[i - 1][j - k * prices[i - 1]] + k * prices[i - 1]
                max_value_without_current = max(max_value_without_current, max_value_with_current)

            dp[i][j] = max_value_without_current

    # Trace back the optimal order list
    i, j = n, balance
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            # How many pieces we choose from the snack
            count = j // prices[i - 1]
            
            # The choosable snacks
            snack_names = []
            for snack in snacks:
                if snack.price == prices[i - 1]:
                    snack_names.append(snack.name)
            
            # Create new order
            selected_items.append(
                Order(
                    prices[i - 1],
                    count,
                    set(snack_names)
                )
            )
            
            j -= count * prices[i - 1]
        i -= 1
        
    # Optimal value
    optimal_value = sum(order.price * order.count for order in selected_items)
    
    return optimal_value, selected_items

# Loads the menu from the given path
def loadMenu() -> list[Snack]:
    menu = []
    menuYaml = None
    
    try:
        menuYaml = yaml.safe_load(args.menu)

    except ValueError:
        print("Invalid value!")
        sys.exit(1)

    except FileNotFoundError:
        print("File was not found!")
        sys.exit(1)
        
    if args.printMenu:
        bprint.pp(menuYaml)

    menuYaml = menuYaml.get('items')
    
    for item in menuYaml:
        if(item['available']):
            menu.append(
                Snack(
                    name = item['name'],
                    price = item['price'],
                    desired = item['desired'],
                )
            )
        
    return menu

# MAIN
def main():
    if args.balance is None:
        print("Balance was not given!")
        sys.exit(1)
        
    if args.menu is None:
        print("Menu list path was not given!")
        sys.exit(1)
    
    menu = loadMenu()
    optimal_value, selected_items = calcOrder(args.balance, menu)
    
    print(f"Optimal value: {optimal_value} JMF")
    print("Order:")
    for order in selected_items:
        order.show()

if __name__ == "__main__":
    main()
    