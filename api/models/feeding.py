from datetime import datetime
from api.models.db import db

class Feeding(db.Model):
    __tablename__ = 'feedings'
    id = db.Column(db.Integer, primary_key=True)
    # enum constraint limits valid inputs to B, L and D
    meal = db.Column('meal', db.Enum('B', 'L', 'D', name='meal_type'))
    # allows users to select the time and date of a feeding
    date = db.Column(db.DateTime, default=datetime.now(tz=None))
    # timestamp
    created_at = db.Column(db.DateTime, default=datetime.now(tz=None))
    # column for cat_id establishes a "belongs to" relationship between feeding and cat
    cat_id = db.Column(db.Integer, db.ForeignKey('cats.id'))

    def __repr__(self):
      return f"Feeding('{self.id}', '{self.meal}'"

    def serialize(self):
      return {
        "id": self.id,
        "meal": self.meal,
        "cat_id": self.cat_id,
        # formats the date
        "date": self.date.strftime('%Y-%m-%d'),
      }

# method that allows a Feeding model to look at its date column, and compate that value to today's date
    def is_recent_meal(self):
      # if Feeding is scheduled for today's date, return true
      if self.date.strftime('%Y-%m-%d') == datetime.now(tz=None).strftime('%Y-%m-%d'):
        return True