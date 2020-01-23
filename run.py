import os
from flask import Flask, render_template
from flask_pymongo import PyMongo

MONGO_DATA = os.getenv("MONGO_URI")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/allbooks")
def all():
    return render_template("allbooks.html")


if __name__ =="__main__":
    app.run(host=os.getenv("IP"),
       port=int(os.getenv("PORT")),
       debug=True)