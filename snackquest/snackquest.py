import argparse
import sys

from solver import solve_problem


def _init_args():
    # Set the argument flags
    parser = argparse.ArgumentParser(
        prog="Vending Machine Loot Calculator",
        description="From the given budget and menu list calculates the optimal order to leave as less money on the card as possible."
    )
    parser.add_argument("budget", help="The current budget of the card [default JMF]", type=int)
    parser.add_argument("menu", help="Vending machine's menu [.yml, .yaml]", type=argparse.FileType("r"))
    parser.add_argument("-p", "--printMenu", dest="print_menu", action="store_true", help="Prints the menu")
    parser.add_argument("-o", "-out", dest="out_file", type=argparse.FileType("w", encoding="UTF-8"), help="The output file path")
    
    return parser.parse_args()

def main():
    args = _init_args()
    
    if args.budget is None:
        print("budget was not given!")
        sys.exit(1)
        
    if args.menu is None:
        print("Menu list path was not given!")
        sys.exit(1)
        
    if args.out_file is not None:
        sys.stdout = args.out_file
        
    # Solve problem.
    solve_problem(args.budget, args.menu, args.print_menu)

if __name__ == "__main__":
    main()
