import yaml, sys, argparse, logging, time
import beeprint as bprint
from models.snack import Snack
from models.order import Order, Orders
from models.graph import *
from rich.console import Console
from rich.table import Table
from rich.padding import Padding

# Set the argument flags
parser = argparse.ArgumentParser(
    prog="Vending Machine Loot Calculator",
    description="From the given balance and menu list calculates the optimal order to leave as less money on the card as possible."
)
parser.add_argument("balance", help="The current balance of the card [default JMF]", type=int)
parser.add_argument("menu", help="Vending machine's menu [.yml, .yaml]", type=argparse.FileType("r"))
parser.add_argument("-p", "--printMenu", dest="print_menu", action="store_true", help="Prints the menu")
parser.add_argument("-i", "--info", dest="log_info", action="store_true", help="Prints log messages")
parser.add_argument("-l", "--limit", dest="limit", type=int, default=3, help="Possible order solution limit")
parser.add_argument("-o", "-out", dest="out_file", type=argparse.FileType("w", encoding="UTF-8"), help="The output file path")
args = parser.parse_args()

# Set the logging config
if args.log_info:
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARNING)

# Calculates the best order
def _calc_order(balance: int, snacks: list[Snack]):
    orders: list[Orders] = []
    desired_items: list[Order] = []
    
    # Pick out the desired items first
    logging.info("Picking out the desired items...")
    for snack in snacks:
        if snack.desired > 0:
            balance -= snack.price * snack.desired
            snack.tobuy = snack.desired
            desired_items.append(
                Order(
                    snack.price,
                    snack.desired,
                    {snack.name}
                )
            )

        snack.desired = 0
    
    if balance <= 0:
        print("Your balance fall below 0 JMF, too much desired snacks!")
        sys.exit(1)
    
    # Graph algorithm
    distinct_prices = []
    for snack in snacks:
        distinct_prices.append(snack.price)
    distinct_prices = set(distinct_prices)
    
    # Build a graph for one price (start_snack_price)
    #   with this the alg is able to find the best possible solution
    #   it makes the program much faster
    start_snack_price = snacks[0].price
    root = Node(start_snack_price, balance)
    logging.info("Building graph...")
    start_time = time.time()
    build_graph(root, distinct_prices)
    end_time = time.time()
    logging.info(f"Graph building finished! ({round(end_time - start_time, 1)} seconds)")

    # Find the optimal child in graph
    logging.info("Finding the best order list...")
    possible_orders: list[Node] = my_dfs(root)

    # Find the minimal balance    
    min_balance = possible_orders[0].balance
    for po in possible_orders:
        if po.balance < min_balance:
            min_balance = po.balance
    
    minimals = set(filter(lambda o: o.balance == min_balance, possible_orders))
    
    # Create possible orders
    logging.info("Creating order list...")
    limit = args.limit
    for m in minimals:
        
        if(limit <= 0):
            break
        else:
            limit -= 1
        
        total_orders = desired_items.copy()
        total_orders.extend(m.get_order(snacks))
        
        orders.append(
            Orders(
                min_balance,
                total_orders
            )
        )
        total_orders = []
        
    return orders

# Loads the menu from the given yaml file
def load_menu() -> list[Snack]:
    menu = []
    menu_yaml = None
    
    try:
        menu_yaml = yaml.safe_load(args.menu)

    except ValueError:
        print("Invalid value!")
        sys.exit(1)

    except FileNotFoundError:
        print("File was not found!")
        sys.exit(1)
        
    if args.print_menu:
        bprint.pp(menu_yaml)

    menu_yaml = menu_yaml.get('items')
    
    for item in menu_yaml:
        if(item['available']):
            menu.append(
                Snack(
                    name = item['name'],
                    price = item['price'],
                    desired = item['desired'],
                )
            )
        
    return menu

def _print_solutions(solutions: list[Orders]):
    console = Console()
    
    for solution_index in range(len(solutions)):
        table = Table(
            title=f"Solution #{solution_index + 1}",
            caption=f"Final balance: {solutions[solution_index].balance} JMF",
            )
        
        # Add columns
        table.add_column("Price")
        table.add_column("Count")
        table.add_column("Snack Options")
        
        # Add rows
        for order in solutions[solution_index].orders:
            table.add_row(str(order.price), str(order.count), order.get_snacks())
        
        # Print table
        console.print(Padding("", (1, 0, 0, 0)))
        console.print(table)

# MAIN
def main():
    if args.balance is None:
        print("Balance was not given!")
        sys.exit(1)
        
    if args.menu is None:
        print("Menu list path was not given!")
        sys.exit(1)
    
    logging.info("Loading menu...")
    menu = load_menu()
    logging.info("Menu loaded!")
    
    possible_orders = _calc_order(args.balance, menu)
    logging.info("Searching finished!")
    
    if args.out_file is not None:
        sys.stdout = args.out_file
        
    """ print("Possible orders:")
    for po in possible_orders:
        po.show() """
    
    _print_solutions(possible_orders)

if __name__ == "__main__":
    main()
    