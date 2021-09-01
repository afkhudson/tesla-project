from flask import Flask, redirect, url_for, render_template
import pandas as pd
import glob
import time
import os
from datetime import date

css1 = 'normalize.css'
css2 = 'webflow.css'
css3 = 'used-tesla-model.webflow.css'

test = "YOLOOOOO"
print('hello')

tesla_list_of_files = glob.glob('all_data/*')
tesla_latest = max(tesla_list_of_files, key=os.path.getctime)
vehicle_data = pd.read_csv(tesla_latest)
vehicle_rows = vehicle_data.iterrows()

for index, row in vehicle_rows:
    print(row['url'])


app = Flask(__name__)

@app.route("/")
def home():
    return "Hello this is the main page"

@app.route("/vehicles/")
def vehicles():
    return render_template("test.html", data=vehicle_data, css1=css1, css2=css2, css3=css3)


@app.route("/<name>/")
def user(name):
    return f"Hello {name}"

@app.route("/admin/")
def admin():
    return redirect(url_for("user", name="Admin!"))

if __name__ == "__main__":
    app.run()
