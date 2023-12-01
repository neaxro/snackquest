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
def calcOrder(menu: list[Snack]):
    order: Order = Order(args.balance, menu)
    
    for snack in order.snacks:
        if snack.desired > 0:
            order.balance -= snack.price * snack.desired
            snack.tobuy = snack.desired

        snack.desired = 0
    
    if order.balance <= 0:
        print("Your balance fall below 0 JMF, too much desired snacks!")
        sys.exit(1)
    
    # Smart algorithm
    # table[row][col]

    n = len(order.snacks)
    w = [snack.price for snack in order.snacks]
    #v = [snack.price for snack in order.snacks]
    v = [1]*n
    W = order.balance
    m = [[0 for i in range(W)] for j in range(n)]
        
    w.sort()
    
    for i in range(1, n):
        for j in range(1, W):
            if w[i] > j:
                m[i][j] = m[i-1][j]
            else:
                m[i][j] = max(m[i-1][j], m[i-1][j-w[i]] + v[i])
        
    counts = [row[-1] for row in m]
    
    print(w)
    print(counts)
    
    sum = 0
    for i in range(n):
        sum += w[i] * counts[i]
        
    print(f"sum: {sum}")
    
    return order

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
    order = calcOrder(menu)
    
    order.show()

if __name__ == "__main__":
    main()
    