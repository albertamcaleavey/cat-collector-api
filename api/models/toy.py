from datetime import datetime
from api.models.db import db

# # association table that allows association of Toys to cats M:M relationship
# # creates a relationship by storing the primary keys of a single cat and toy
# class Association(db.Model):
#     __tablename__ = 'associations'
#     id = db.Column(db.Integer, primary_key=True)
#     # stores primary key of single cat 
#     cat_id = db.Column(db.Integer, db.ForeignKey('cats.id', ondelete='cascade'))
#     # stores primary key of single toy 
#     toy_id = db.Column(db.Integer, db.ForeignKey('toys.id', ondelete='cascade'))
#     # ondelete = 'cascade' ensures that a row in our associations table is removed whenever a parent cat or toy is deleted 


class Association(db.Model):
    __tablename__ = 'associations'
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('cats.id', ondelete='cascade'))
    toy_id = db.Column(db.Integer, db.ForeignKey('toys.id', ondelete='cascade'))




class Toy(db.Model):
    __tablename__ = 'toys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
      return f"Toy('{self.id}', '{self.name}'"

    def serialize(self):
      toy = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return toy