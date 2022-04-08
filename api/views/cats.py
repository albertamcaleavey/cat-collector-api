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