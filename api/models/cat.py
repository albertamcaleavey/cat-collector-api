from datetime import datetime
from api.models.db import db

# class Cat(db.Model):
#     __tablename__ = 'cats'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     breed = db.Column(db.String(100))
#     description = db.Column(db.String(250))
#     age = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

#           # RELATIONSHIPS

#     # establish a 'Has Many' relationship with feeding (so a cat has many feedings)
#     # requires a foreign key on the child model (cat_id on feeding)
#     # allows us to grab all associated feeding models when we query for a cat
#     feedings = db.relationship("Feeding", cascade='all')
#     # cascade - option that ensures that if we delete a parent cat from the db, any associated feedings are also removed

#     # allows us to find all associated toys when querying for a cat
#     toys = db.relationship("Toy", secondary="associations")
#     # secondary='associations' lets us specify which table is acting as an intermediary between cats and toys


#     def __repr__(self):
#       return f"Cat('{self.id}', '{self.name}'"

#     # Existing serialize method:
#     # def serialize(self):
#     #   cat = {c.name: getattr(self, c.name) for c in self.__table__.columns}
#     #   return cat

#     # Refactored serialize method:
#     # method that adds each key value pair in the model to a dictionary = giving us the ability to view our data in JSON serializable format (so we can send JSON data to front end)
#     def serialize(self):
#       cat = {c.name: getattr(self, c.name) for c in self.__table__.columns}
#       # now includes a feedings property in the cat dictionary 
#       feedings = [feeding.serialize() for feeding in self.feedings] 
#       toys = [toy.serialize() for toy in self.toys]
#       cat['feedings'] = feedings
#       cat['toys'] = toys
#       return cat

#     # method that detects whether or not the cat has been fed for the day
#     def fed_for_today(self):
#       # iterate through the associated feedings
#       # if three or more feedings are recent, the cat is fed for the day
#       if len([f for f in self.feedings if f.is_recent_meal() == True]) >= 3:
#         return True
#       else:
#         return False

class Cat(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    breed = db.Column(db.String(100))
    description = db.Column(db.String(250))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    # Relationships:
    feedings = db.relationship("Feeding", cascade='all')
    toys = db.relationship("Toy", secondary="associations") # <=== Here ===

    def __repr__(self):
      return f"Cat('{self.id}', '{self.name}'"

    def serialize(self):
      cat = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      feedings = [feeding.serialize() for feeding in self.feedings] 
      toys = [toy.serialize() for toy in self.toys] # <=== Here ===
      cat['feedings'] = feedings
      cat['toys'] = toys # <=== Here ===
      return cat

    def fed_for_today(self):
      if len([f for f in self.feedings if f.is_recent_meal() == True]) >= 3:
        return True
      else:
        return False
