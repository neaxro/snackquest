import pulp
import beeprint as bprint

from enum import Enum
from rich.console import Console
from rich.table import Table
from rich.padding import Padding

class TargetFunction(Enum):
    MINIMALIZE_REMAINING_MONEY = "minremoney"
    MAXIMIZE_CANDIES = "maxcandy"
    
def _minimalize_remaining_money(variables: dict, data, budget) -> pulp.LpProblem:
    # Init problem
    problem = pulp.LpProblem("MINIMALIZE_REMAINING_MONEY", pulp.LpMaximize)
    # Define target function
    problem += pulp.lpSum(variables[item['name']] * item['price'] for item in data['items'] if item['available'])
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
    
    return problem

def _maximize_candies(variables: dict, data, budget) -> pulp.LpProblem:
    # Init problem
    problem = pulp.LpProblem("MAXIMIZE_CANDIES", pulp.LpMaximize)
    # Define target function
    problem += pulp.lpSum(variables[item['name']] for item in data['items'] if item['available'])    # Limit: Money
    problem += pulp.lpSum(
        variables[item['name']] * item['price']
        for item in data['items']
        if item['available']
    ) <= budget
    # Limit: Min count of specific candies.
    for item in data['items']:
        if item['available']:
            problem += variables[item['name']] >= item['desired']
    
    return problem

def solve_problem(budget, data, target_funcion: TargetFunction, print_menu=False, headless=False):
    if print_menu:
        bprint.pp(data)    

    # Use only the available candies.
    variables = {}
    for item in data['items']:
        if item['available']:
            variables[item['name']] = pulp.LpVariable(
                item['name'], lowBound=0, cat='Integer'
            )

    # Create the problem based on the goal of the user.
    if target_funcion == TargetFunction.MINIMALIZE_REMAINING_MONEY:
        problem = _minimalize_remaining_money(variables, data, budget)
        # problem.sense = pulp.LpMinimize
    elif target_funcion == TargetFunction.MAXIMIZE_CANDIES:
        problem = _maximize_candies(variables, data, budget)
    else:
        raise ValueError(f"Unknown target function: {target_funcion}")

    # Solve.
    problem.solve(pulp.PULP_CBC_CMD(msg=False))

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
        return None

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
