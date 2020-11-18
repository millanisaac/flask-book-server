import os
import requests
import sqlalchemy
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from Person import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
app.config["SECRET_KEY"] = "Hello"
# db = scoped_session(sessionmaker(bind=engine))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET" and session.get("username") is not None:
        return redirect(url_for("home"))
    if request.method == "POST":
        session["username"] = None
    return render_template("login.html")

@app.route("/home", methods=["POST", "GET"])
def home():
    if session.get("username") is None:
        if request.method == "GET":
            return redirect(url_for("index"))

        username = request.form.get("username")
        password = request.form.get("password")
        if request.form["submit_button"] == "Create Account":
            if password == "" or username == "":
                return "either password or username is left blank"
            try:
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                return "username already taken"
        else:
            if User.query.filter_by(username=username).first() is None or User.query.filter_by(
                    username=username).first().password != password:
                return "error"
        session["username"] = username
    return render_template("home.html", username=session["username"])


@app.route("/searchresults", methods=["POST"])
def searchresults():
    searchresults = "%" + request.form["searchresult"] + "%"
    Books = Book.query.filter(Book.title.like(searchresults)).all()
    return render_template("books.html", books=Books)


@app.route("/searchresults/<string:name>/<int:id>", methods=["post", "get"])
def book(name, id):

    book = Book.query.filter_by(id=id).first()

    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
                         params={"key": "dYNUgqGWiVohadlSL6cGg", "isbns": "9781632168146"}).json()['books'][0]
    book.average_score = float(goodreads["average_rating"])
    book.review_count = goodreads['work_ratings_count']
    if request.method == "POST":
        book.add_review(session["username"], request.form.get("review"))

    return render_template("book.html", book=book, reviews=book.reviews, user=session["username"])

@app.route("/api/<string:isbn>", methods=["get"])
def api(isbn):

    book = Book.query.filter_by(isbn = isbn).first()
    test = book.reviews
    reviews = []
    for review in test:
        reviews.append(review.review)
    return jsonify({
        "author": book.author,
        "title": book.title,
        "reviews": reviews
             })
