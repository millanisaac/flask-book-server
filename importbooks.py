import csv
from Person import *
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://zdhpcsmnixyjjo:d220d07c669da0a838f33ccdc9d08a16b3e7d64b27f09311c55163ff6d5130a4@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d23av41pu1d6bc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open('books.csv')
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        book = Book(title=title, author=author, year=int(year), isbn=isbn, review_count=None, average_score=None)
        db.session.add(book)
        print(title, author, year, isbn)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()