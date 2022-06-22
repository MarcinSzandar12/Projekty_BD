from app import db

class Author(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   full_name = db.Column(db.String(200), index=True)

   def __str__(self):
       return f"<Author {self.full_name}>"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", backref="books", lazy="dynamic")

    def __str__(self):
       return f"<Book {self.title} {self.author}>"