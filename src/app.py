"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
john_jackson = {
    "id": jackson_family._generateId(),
    "name": "John Jackson",
    "age": 33,
    "lucky_members": [7, 13, 22]
}
jane_jackson = {
    "id": jackson_family._generateId(),
    "name": "Jane Jackson",
    "age": 35,
    "lucky_members": [10, 14, 3]
}
jimmy_jackson = {
    "id": jackson_family._generateId(),
    "name": "Jimmy Jackson",
    "age": 5,
    "lucky_members": [1]
}
jackson_family.add_member(john_jackson)
jackson_family.add_member(jane_jackson)
jackson_family.add_member(jimmy_jackson)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    response_body = jackson_family.get_all_members()
    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    response_body = jackson_family.get_member(id)

    if response_body is None:
        raise APIException('Member not found', status_code=404)
    
    return jsonify(response_body), 200


@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.get_json()

    jackson_family.add_member(new_member)

    return jsonify("New member added"), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)

    if deleted is False:
        raise APIException('Member not found', status_code=404) 

    return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)