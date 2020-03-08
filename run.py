import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import string
import random


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'books-project'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


@app.route("/")
def index():
    
    books = list(mongo.db.books.find())
    
    random_book = random.choice(books)
    
    return render_template("index.html", random_book=random_book)
    
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
    
@app.route("/deletereview/<book_id>/<username>/<review_text>")
def delete_review(book_id, username, review_text):
    
    mongo.db.books.update_one({"_id": ObjectId(book_id)}, { "$pull": { "reviews": { "username": username, "review_text": review_text }}})
    
    return redirect(url_for("book", book_id=book_id))
    
@app.route("/editreview/<book_title>/<book_id>/<username>/<review_text>")
def edit_review(book_title, book_id, username, review_text):
    
    
    
    return render_template("editreview.html", book_title=book_title, book_id=book_id, username=username, review_text=review_text)
    
@app.route("/editreviewdata/<book_id>/<username>/<review_text>", methods=['POST'])    
def edit_review_data(book_id, username, review_text):
    
    # remove the original review
    mongo.db.books.update_one({"_id": ObjectId(book_id)}, { "$pull": { "reviews": { "username": username, "review_text": review_text }}})
    
    form = request.form.to_dict()
    
    # add the edited review
    mongo.db.books.update_one({"_id": ObjectId(book_id)}, { "$push": { "reviews": { "username": form['username'], "review_text": form['review_text'] }}})
    
    return redirect(url_for("book", book_id=book_id))

@app.route("/searchresults", methods=['POST'])
def search_results():
    
    form_data = request.form.to_dict()
    search_term = form_data['searchbox']
    
    reg_exp = ""
    
    terms = search_term.split()
    
    """
    want to create a regular expression that has all the search terms
    and ignores the case of the characters. Punctuation and numbers 
    are ignored from the search term.
    """
    for str in terms:
        
        str = str.lower()
        reg = ""
        
        for letter in str:
            
            if letter in string.ascii_letters:
                
                reg += "[" + letter + letter.upper() + "]"
                
        
        print("Reg = " +reg +"length: ")
        print(len(reg))
        
        if not reg_exp and reg:
            reg_exp += reg
        elif reg:
            reg_exp += "|" + reg
            
    print("Reg exp is: " +reg_exp)
    
    if reg_exp:
        results = list(mongo.db.books.find({ "$or": [{"title": { "$regex": reg_exp}},{ "author": { "$regex": reg_exp}}]}))
    else:
        results = []
    
    return render_template("searchresults.html", search_term=search_term, results=results)

if __name__ =="__main__":
    app.run(host=os.getenv("IP"),
       port=int(os.getenv("PORT")),
       debug=False)