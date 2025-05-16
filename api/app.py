import os
import yaml
import json

from flask import Flask, jsonify, request
from cli.solver import solve_problem, TargetFunction

machines_path = os.getenv("MACHINE_INVENTORY_PATH", f"{__package__}/machines")

app = Flask(__name__)

@app.get(
    "/machines/<name>"
)
def get_machine_inventory(name):
    path = f"{machines_path}/{name}"
    try:
        if not os.path.isfile(path):
            return {
                "error": f"Machine does not found with name: {name}"
            }, 404
        with open(path, "r") as f:
            content = yaml.safe_load(f.read())        
            return jsonify(content), 200
    except Exception as e:
        return {
            "error": str(e)
        }, 500

@app.get(
    "/machines"
)
def get_machines():
    try:
        machines = os.listdir(machines_path)
        return jsonify(machines), 200
    except Exception as e:
        return {
            "error": str(e)
        }, 500

@app.post(
    "/solve"
)
def solve():
    budget = request.args.get('budget', type=int)
    target_function = request.args.get('target_function', type=str)
    inventory = request.json
    
    if budget <= 0:
        return {
            "error": f"Budget must be a positive number!"
        }, 500
    
    if target_function not in ["minremoney", "maxcandy"]:
        return {
            "error": f"Target function not found: {target_function}"
        }, 404

    try:
        result = solve_problem(
            budget=budget,
            data=inventory,
            target_funcion=TargetFunction(target_function),
            headless=True,
            print_menu=False
        )
        
        if not result:
            return {
                "error": "There is no solution!"
            }, 204
        
        return jsonify(result), 200
        
    except json.JSONDecodeError as e:
        return {
            "error": str(e)
        }, 500

if __name__ == "__main__":
    app.run(
        "0.0.0.0",
        port=5000,
        debug=True
    )
