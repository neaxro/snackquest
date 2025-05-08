import pulp
import beeprint as bprint

from rich.console import Console
from rich.table import Table
from rich.padding import Padding


def solve_problem(budget, data, print_menu=False, headless=False):
    if print_menu:
        bprint.pp(data)

    problem = pulp.LpProblem("Maximize_Candies", pulp.LpMaximize)

    # Init variables
    variables = {}
    for item in data['items']:
        if item['available']:  # Use only the available candies.
            variables[item['name']] = pulp.LpVariable(
                item['name'], lowBound=0, cat='Integer'
            )

    # Target function: Maxminal candy count.
    problem += pulp.lpSum(variables[item['name']] for item in data['items'] if item['available'])

    # Limit: Money
    problem += pulp.lpSum(
        variables[item['name']] * item['price']
        for item in data['items']
        if item['available']
    ) <= budget

    # Limit: Min count of specific candies.
    for item in data['items']:
        if item['available']:
            problem += variables[item['name']] >= item['desired']

    # Solve.
    problem.solve()

    # Show results.
    if problem.status == pulp.LpStatusOptimal:
        final_items = []

        total_candies = 0
        total_cost = 0

        for item in data['items']:
            if item['available']:
                count = int(variables[item['name']].varValue)
                total_candies += count
                total_cost += count * item['price']
                
                # Collect final items.                
                final_items.append(
                    {
                        'name': item['name'],
                        'count': count,
                        'unit_price': item['price']
                    }
                )
        
        if not headless:
            _print_solution(budget, final_items, total_candies, total_cost)
        
        return {
            'budget': budget,
            'final_items': final_items,
            'total_candies': total_candies,
            'total_cost': total_cost
        }
    else:
        print("No solution found.")

def _print_solution(budget, final_items, total_candies, total_cost):
    console = Console()
    
    # Create table
    table = Table(
        title=f"The Optimal Solution",
        caption=f"Initial budget: {budget}",
    )
    
    # Add columns
    table.add_column("Snack Options")
    table.add_column("Count")
    table.add_column("Unit price", justify="right")
    
    # Add rows
    for item in final_items:
        table.add_row(
            item['name'],
            str(item['count']),
            str(item['unit_price'])
        )

    # Add footer
    table.add_section()
    table.add_row("Total", str(total_candies), str(total_cost))
    table.add_row("Remaining", "", str(budget-total_cost))
    table.add_section()
    table.add_row("Initial budget", "", str(budget))

    # Print table
    console.print(Padding("", (0, 0, 0, 0)))
    console.print(table)
