from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    review_count = db.Column(db.Integer, nullable=True)
    average_score = db.Column(db.Float, nullable=True)
    reviews = db.relationship("Reviews", backref="book", lazy=True)

    def add_review(self, username, reviews):
        review = Reviews(user=username, book_id=self.id, review=reviews)
        db.session.add(review)
        db.session.commit()


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    review = db.Column(db.String, nullable=False)


