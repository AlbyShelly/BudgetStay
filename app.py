from algorithms.cheriyan import budget_stay_decision_tree
#from algorithms.alby import budget_stay_linear_regression
from flask import Flask, render_template, request, redirect
from test import get_rows
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "GET":
        return render_template("index.html")
   
    
    else:
        
        acNonAc = request.form.get("acNonAc")
        location = request.form.get("location")
        cost = request.form.get("cost")
        cursor = get_rows(location, cost, acNonAc)
        print(cursor, "cursor")
        return render_template("result.html", cursor = cursor)

@app.route("/alby", methods=["GET", "POST"])
def alby():

    acNonAc = request.form.get("acNonAc")
    location = request.form.get("location")
    cost = request.form.get("cost")

    #predicted_cost = budget_stay_linear_regression(location, acNonAc)
    predicted_cost = budget_stay_decision_tree(location, acNonAc)
    
    rows = get_rows(location, cost, acNonAc)
    cursor = []
    for row in rows:
        cursor.append(row)
    cursor = sorted(cursor, key = lambda x: abs(predicted_cost - x["cost"]))
    
    return render_template("result.html", cursor = cursor) 
