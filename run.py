import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


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
    

@app.route("/book/<book_id>")
def book(book_id):
    
    my_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    
    return render_template("book.html", book=my_book)

@app.route("/addreview/<book_id>")
def add_review(book_id):
    
    current_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    
    return render_template("addreview.html", current_book=current_book)
    
@app.route("/addreviewdata/<book_id>", methods=['POST'])
def add_review_data(book_id):
    
    form = request.form.to_dict()
    
    mongo.db.books.update_one({"_id": ObjectId(book_id)}, { "$push": { "reviews": { "username": form['username'], "review_text": form['review_text'] }}})
    
    return redirect(url_for("book", book_id=book_id))
    
@app.route("/deletereview/<book_id>")
def delete_review(book_id):
    
    print("Book ID:" + book_id)
    
    return redirect(url_for("book", book_id=book_id))


if __name__ =="__main__":
    app.run(host=os.getenv("IP"),
       port=int(os.getenv("PORT")),
       debug=True)