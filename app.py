from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/flask_mysql_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db  = SQLAlchemy(app)

if __name__=='__main__':
    with app.app_context():
        app.run(debug=True)

#Model
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return jsonify({"message": "Hello, Its Wainaina"})

#http://127.0.0.1:5000/persons
@cross_origin()
@app.route("/persons", methods=["POST"])
def create_person():
    data = request.json

    name = data['name']
    age = data['age']
    city = data['city']

    person = Person(name=name, age=age, city=city)
    db.session.add(person)
    db.session.commit()

    return jsonify({"message": "Person created successfully", "Person": data})

#http://127.0.0.1:5000/persons-get
@cross_origin()
@app.route("/persons-get", methods=["GET"])
def get_persons():
    all_persons = []
    persons = Person.query.all()
    for person in persons:
        results = {
            "id": person.id,
            "name": person.name,
            "age": person.age,
            "city": person.city,
        }
        all_persons.append(results)

    return jsonify(
        {
            "success": True,
            "persons": all_persons,
            "total": len(persons)
        }
    )

#http://127.0.0.1:5000/persons/1
@cross_origin()  
@app.route("/persons/<int:id>", methods = ["PATCH"])
def update_person(id):
    person = Person.query.get(id)
    name = request.json['name']
    age = request.json['age']
    city = request.json['city']

    if person is None:
        abort(404)
    else:
        person.name = name
        person.age = age
        person.city = city
        db.session.add(person)
        db.session.commit()
        return jsonify({"success": True, "response": "Person Details updated", "Person": request.json})

#http://127.0.0.1:5000/persons/1
@cross_origin()  
@app.route("/persons/<int:id>", methods = ["DELETE"])
def delete_persons(id):
    person = Person.query.get(id)

    if person is None:
        abort(404)
    else:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"success": True, "response": "Person deleted successfully"})

