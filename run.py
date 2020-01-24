import os
from flask import Flask, render_template
from flask_pymongo import PyMongo


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'books-project'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/allbooks")
def all():
    
    all_books = mongo.db.books.find()
    
    return render_template("allbooks.html", all_books=all_books)


if __name__ =="__main__":
    app.run(host=os.getenv("IP"),
       port=int(os.getenv("PORT")),
       debug=True)