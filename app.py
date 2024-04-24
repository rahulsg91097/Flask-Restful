from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
import psycopg2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/flask_restful_db"
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# GET, POST, PUT, PATCH, DELETE
class PeopleResource(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "name": user.name,
                "age": user.age
            }
            user_list.append(user_data)
        return jsonify(user_list)

    def post(self, ):
        new_person = User(
            name=request.json["name"],
            age = request.json["age"]
        )
        db.session.add(new_person)
        db.session.commit()
        return make_response(jsonify({
            "id": new_person.id,
            "name": new_person.name,
            "age": new_person.age
        }), 201) 

class PersonResource(Resource):
    def get(self, person_id):
        user = User.query.get(person_id)
        if user:
            user_details = {
                "id": user.id,
                "name": user.name,
                "age": user.age
            }
            return make_response(jsonify(user_details), 200)
        return jsonify({"message": "User does not exists"})
    
    def put(self, person_id):
        user = User.query.get(person_id)
        user.name = "vinsmoke Sanjhi"
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({
            "id": user.id,
            "name": user.name,
            "age": user.age
        }), 201)
    
    def delete(self, person_id):
        user = User.query.get(person_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "user deleted successfully"})
    
api.add_resource(PeopleResource, "/people")
api.add_resource(PersonResource, "/people/<int:person_id>")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)