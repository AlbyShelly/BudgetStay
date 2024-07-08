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
       


