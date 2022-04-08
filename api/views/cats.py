from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.cat import Cat
from api.models.feeding import Feeding
from api.models.toy import Toy
from api.models.toy import Association

cats = Blueprint('cats', 'cats')

#----------------------------------------------

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

  #----------------------------------------------

# indexing cats route
@cats.route('/', methods=["GET"])

# indexing cats controller
def index():
  # find all of the cats and store them in a variable
  cats = Cat.query.all()
  # return a JSON response with all of the serialized cats
  return jsonify([cat.serialize() for cat in cats]), 200

#----------------------------------------------

# show cat route
# @cats.route('/<id>', methods=["GET"])

# # show cat controller
# def show(id):
#   # .filter allows you to search by any column in a table
#   cat = Cat.query.filter_by(id=id).first()
#   cat_data = cat.serialize()
#   # add fed property to cat_data = a boolean value which is returned by the fed_for_today method
#   cat_data["fed"] = cat.fed_for_today()
#   # separate query for all toys not yet associated with this cat
#   toys = Toy.query.filter(Toy.id.notin_([toy.id for toy in cat.toys])).all()
#   toys=[toy.serialize() for toy in toys]
#   return jsonify(cat=cat_data, available_toys=toys), 200

@cats.route('/<id>', methods=["GET"])
def show(id):
  cat = Cat.query.filter_by(id=id).first()
  cat_data = cat.serialize()
  cat_data["fed"] = cat.fed_for_today()

  # Add the following:
  toys = Toy.query.filter(Toy.id.notin_([toy.id for toy in cat.toys])).all()
  toys=[toy.serialize() for toy in toys]

  return jsonify(cat=cat_data, available_toys=toys), 200 # <=== Include toys in response

#----------------------------------------------

# update cat route
@cats.route('/<id>', methods=["PUT"])

# update cat controllers
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

#----------------------------------------------

# delete route
@cats.route('/<id>', methods=["DELETE"])

# delete controller
@login_required
def delete(id):
  profile = read_token(request)
  cat = Cat.query.filter_by(id=id).first()

  if cat.profile_id != profile["id"]:
    return 'Forbidden', 403
# deletes the row (cat instance) from the table
  db.session.delete(cat)
  db.session.commit()
  # returns a response with a success message, since you don't need to return data
  return jsonify(message="Success"), 200

#----------------------------------------------

# create feeding route
@cats.route('/<id>/feedings', methods=["POST"])

# create feeding controller
@login_required
def add_feeding(id):
  data = request.get_json()
  data["cat_id"] = id

  profile = read_token(request)
  cat = Cat.query.filter_by(id=id).first()

  if cat.profile_id != profile["id"]:
    return 'Forbidden', 403

  feeding = Feeding(**data)
  
  db.session.add(feeding)
  db.session.commit()

  cat_data = cat.serialize()
  # adds a fed property to the cat_data object - use this boolean for conditional rendering in React
  cat_data["fed"] = cat.fed_for_today()

  return jsonify(cat_data), 201

#----------------------------------------------

# route
@cats.route('/<cat_id>/toys/<toy_id>', methods=["LINK"])

#controller
@login_required
def assoc_toy(cat_id, toy_id):
  data = { "cat_id": cat_id, "toy_id": toy_id }

  profile = read_token(request)
  cat = Cat.query.filter_by(id=cat_id).first()
  
  if cat.profile_id != profile["id"]:
    return 'Forbidden', 403

  assoc = Association(**data)
  db.session.add(assoc)
  db.session.commit()

  cat = Cat.query.filter_by(id=cat_id).first()
  return jsonify(cat.serialize()), 201
