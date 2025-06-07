import os
import yaml
import json
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from cli.solver import solve_problem, TargetFunction
from api.utils.config import config
from api.utils.metrics import count_requests, latency_request, time_request
from api.utils.logging_config import setup_logger

def setup_app():
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    setup_logger(app)

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/metrics': make_wsgi_app()})

    cors_origins = config.CORS_ORIGINS.split(',') if config.CORS_ORIGINS else "*"
    
    CORS(app,
         resources={r"/*": {"origins": cors_origins}},
         supports_credentials=True,
         allow_headers="*",
         methods=["GET", "POST", "OPTIONS"])

    app.logger.info(f"Running with CORS Origins: {cors_origins}")
    
    return app, app.logger


app, logger = setup_app()


@app.route("/machines/<name>", methods=["GET"])
@latency_request
@count_requests
@time_request
def get_machine_inventory(name):
    path = f"{config.MACHINE_INVENTORY_PATH}/{name}"
    logger.debug(f"Received request to fetch inventory for machine: {name}")
    logger.debug(f"Constructed file path: {path}")

    try:
        if not os.path.isfile(path):
            logger.warning(f"Machine inventory file not found: {path}")
            return {
                "error": f"Machine does not found with name: {name}"
            }, 404
        with open(path, "r") as f:
            content = yaml.safe_load(f.read())
            logger.info(f"Successfully loaded inventory for machine: {name}")
            return jsonify(content), 200
    except Exception as e:
        logger.exception(f"Error while loading machine inventory for: {name}")
        return {
            "error": str(e)
        }, 500


@app.route("/machines", methods=["GET"])
@latency_request
@count_requests
@time_request
def get_machines():
    logger.debug("Received request to fetch available machines.")
    try:
        machines = os.listdir(config.MACHINE_INVENTORY_PATH)
        logger.info(f"Successfuly fetched available machines ({len(machines)})!")
        return jsonify(machines), 200
    except Exception as e:
        logger.exception(f"Error while fetching available machines!")
        return {
            "error": str(e)
        }, 500

@app.route("/solve", methods=["POST"])
@latency_request
@count_requests
@time_request
def solve():
    budget = request.args.get('budget', type=int)
    target_function = request.args.get('target_function', type=str)
    inventory = request.json
    
    logger.debug(f"Received request to solve problem. Budget: {budget}, Target function: {target_function}")
    
    if budget <= 0:
        logger.warning(f"Budget is not a positive number: {budget}!")
        return {
            "error": f"Budget must be a positive number!"
        }, 500
    
    if target_function not in ["minremoney", "maxcandy"]:
        logger.warning(f"Target function not found: {target_function}!")
        return {
            "error": f"Target function not found: {target_function}"
        }, 404

    try:
        logger.info(f"Solving problem.\t [{target_function}] Budget: {budget}")
        result = solve_problem(
            budget=budget,
            data=inventory,
            target_funcion=TargetFunction(target_function),
            headless=True,
            print_menu=False
        )
        
        if not result:
            logger.warning(f"Solution not found with given criteria! [{target_function}] Budget: {budget}")
            return {
                "error": "There is no solution!"
            }, 204
        
        logger.info(f"Problem solved!\t [{target_function}] Budget: {budget}->{result['budget']-result['total_cost']}, Total candies: {result['total_candies']}")
        return jsonify(result), 200
        
    except json.JSONDecodeError as e:
        logger.exception(f"Error while solving problem!")
        return {
            "error": str(e)
        }, 500

if __name__ == "__main__":
    app.run(
        host=config.APP_HOST,
        port=config.APP_PORT,
        debug=config.APP_DEBUG
    )
