from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.cat import Cat

cats = Blueprint('cats', 'cats')

# create cats route
@cats.route('/', methods=["POST"])

# create cats controller
@login_required
def create():
  # parse the incoming JSON request data and store it in a variable
  data = request.get_json()
  # retrieve a user's profile data with the read_token middleware and assign it to a variable
  profile = read_token(request)
  # add a profile_id property to data (like adding an author property to req.body in Express)
  data["profile_id"] = profile["id"]
  # pass the updated data dictionary to the Cat model, which creates the new resource in our database
  cat = Cat(**data)
  # add and commit the changes to the database
  db.session.add(cat)
  db.session.commit()
  # return a JSON response with the newly created cat data and status code of 201 **make sure to include status code in projects!!
  return jsonify(cat.serialize()), 201


# indexing cats route
@cats.route('/', methods=["GET"])

# indexing cats controller
def index():
  # find all of the cats and store them in a variable
  cats = Cat.query.all()
  # return a JSON response with all of the serialized cats
  return jsonify([cat.serialize() for cat in cats]), 200


# show cat route
@cats.route('/<id>', methods=["GET"])

# show cat controller
@cats.route('/<id>', methods=["GET"])
def show(id):
  # .filter allows you to search by any column in a table
  cat = Cat.query.filter_by(id=id).first()
  cat_data = cat.serialize()
  return jsonify(cat=cat_data), 200


# update cat route
@cats.route('/<id>', methods=["PUT"])

# update cat controllers
@cats.route('/<id>', methods=["PUT"]) 
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  cat = Cat.query.filter_by(id=id).first()
# ensures that only the user who created the cat can update it
  if cat.profile_id != profile["id"]:
    # if its not the right user, return a 403
    return 'Forbidden', 403
# for loop that helps us update the properties of a cat for however many keys were provided in the form data
  for key in data:
    # accepts 3 args:
    # cat = object you want to change
    # key = property we want to set
    # data[key = the value we want to apply to a given property)
    setattr(cat, key, data[key])

  db.session.commit()
  return jsonify(cat.serialize()), 200



