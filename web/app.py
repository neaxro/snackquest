import yaml
import os
import logging

from flask import Flask, render_template, request, abort, send_from_directory
from snackquest.solver import solve_problem, TargetFunction

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def _get_machines():
    return os.listdir("./web/templates/machines/")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    machines = _get_machines()
    if request.form:
        try:
            budget = int(request.form.get("budget"))
            target_function = TargetFunction(str(request.form.get("targetFunction")))
            menu = yaml.safe_load(request.form.get("menu"))
            
            result = solve_problem(budget, menu, target_function, headless=True)
            print(result)

            return render_template("calculator.html", result=result, machines=machines)
        except Exception as e:
            return render_template("calculator.html", error=e)
    else:
        return render_template("calculator.html", machines=machines)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/machines/<filename>")
def get_machine_file(filename):
    safe_path = os.path.join("./web/templates/machines", filename)
    print(safe_path)
    print(os.path.isfile(safe_path))
    if os.path.isfile(safe_path) and filename.endswith(".yaml"):
        return send_from_directory("./templates/machines", filename)
    abort(404)


@app.route("/machines")
def machines():
    machines = _get_machines()
    return render_template("machines.html", machines=machines)

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0"
    )

