import yaml

from flask import Flask, render_template, request
from snackquest.solver import solve_problem

app = Flask(__name__)

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.form:
        try:
            budget = int(request.form.get("budget"))
            menu = yaml.safe_load(request.form.get("menu"))
            
            result = solve_problem(budget, menu, headless=True)
            print(result)

            return render_template("calculator.html", result=result)
        except Exception as e:
            return render_template("calculator.html", error=e)
    else:
        return render_template("calculator.html")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/machines")
def machines():
    return render_template("machines.html")

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0"
    )
