import os
import requests

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/book/<int:isbn>")
def get_book_info(isbn):
    #make sure isbn exists in database
    book = db.execute("SELECT * FROM books WHERE isbn = isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html", message="No book in database for that isbn.")

    #Get info from goodreads API
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "RHUix4sDcDH9V9PfN3jqg", "isbns": book.isbn}).json()["books"][0]
    ratings_count = res["ratings_count"]
    average_rating = res["average_rating"]

    return render_template("detail.html", book=book,ratings_count=ratings_count, average_rating=average_rating)


@app.route("/all")
def index():
    #prints all the books in the database
    books = db.execute("SELECT * from books").fetchall()
    return render_template("index.html", books=books)
