from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.toy import Toy

toys = Blueprint('toys', 'toys')

#----------------------------------------------

# create toys route
@toys.route('/', methods=["POST"])

# create controller
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]

  toy = Toy(**data)
  db.session.add(toy)
  db.session.commit()
  return jsonify(toy.serialize()), 201

#----------------------------------------------

# index toys route
@toys.route('/', methods=["GET"])

# index controller
def index():
  toys = Toy.query.all()
  return jsonify([toy.serialize() for toy in toys]), 201


# show toy route
@toys.route('/<id>', methods=["GET"])

# show toy controller
def show(id):
  toy = Toy.query.filter_by(id=id).first()
  return jsonify(toy.serialize()), 200

#----------------------------------------------

# update toy route
@toys.route('/<id>', methods=["PUT"]) 

# update controller
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  toy = Toy.query.filter_by(id=id).first()

  if toy.profile_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(toy, key, data[key])

  db.session.commit()
  return jsonify(toy.serialize()), 200

#----------------------------------------------

# delete toy route
@toys.route('/<id>', methods=["DELETE"]) 

# delete toy controller
@login_required
def delete(id):
  profile = read_token(request)
  toy = Toy.query.filter_by(id=id).first()

  if toy.profile_id != profile["id"]:
    return 'Forbidden', 403
    
  db.session.delete(toy)
  db.session.commit()
  return jsonify(message="Success"), 200
