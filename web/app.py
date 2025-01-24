import yaml

from flask import Flask, render_template, request
from snackquest.solver import solve_problem

app = Flask(__name__)

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    if request.form:
        try:
            budget = int(request.form.get("budget"))
            menu = yaml.safe_load(request.form.get("menu"))
            
            result = solve_problem(budget, menu, headless=True)
            print(result)

            return render_template("result.html", result=result)
        except Exception as e:
            return f"Error: {e}"

    return "Nope"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
