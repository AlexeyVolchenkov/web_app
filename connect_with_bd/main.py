from flask import Flask, render_template, url_for, request, redirect, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AlEx1902345@localhost/example_db'

db = SQLAlchemy(app)

data = []


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    second_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    first_name_genitive = db.Column(db.String(45), nullable=False)
    second_name_genitive = db.Column(db.String(45), nullable=False)
    mil_ranks_id = db.Column(db.String(36), nullable=False)
    science_ranks_id = db.Column(db.String(36), nullable=False)
    science_levels_id = db.Column(db.String(36), nullable=False)
    post_adress = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<Person {self.id}>"


class Person_contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.String(36), nullable=False)
    contact_types_id = db.Column(db.String(36), nullable=False)
    value = db.Column(db.String(256), nullable=False)

    Person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __repr__(self):
        return f"<Person_contacts {self.id}>"


@app.route('/')
def get_all_users():
    info = Person.query.order_by(Person.id).all()
    data.clear()
    for el in info:
        dict_json = {'id': el.id, 'first_name': el.first_name, 'second_name': el.second_name, 'last_name': el.last_name,
                     'first_name_genitive': el.first_name_genitive, 'second_name_genitive': el.second_name_genitive,
                     'mil_ranks_id': el.mil_ranks_id, 'science_ranks_id': el.science_ranks_id,
                     'science_levels_id': el.science_levels_id, 'post_adress': el.post_adress}
        data.append(dict_json)
    articles = jsonify(data)
    return articles


@app.route('/person/<int:id>')
def get_person(id):
    info_Person = Person.query.get(id)
    dict_json = {'id': info_Person.id, 'first_name': info_Person.first_name, 'second_name': info_Person.second_name, 'last_name': info_Person.last_name,
                     'first_name_genitive': info_Person.first_name_genitive, 'second_name_genitive': info_Person.second_name_genitive,
                     'mil_ranks_id': info_Person.mil_ranks_id, 'science_ranks_id': info_Person.science_ranks_id,
                     'science_levels_id': info_Person.science_levels_id, 'post_adress': info_Person.post_adress}
    return jsonify(dict_json)


@app.route('/person_contacts/<int:id>')
def get_person_contacts(id):
    info_Person_contacts = Person_contacts.query.get(id)
    dict_json = {'person_id': info_Person_contacts.person_id, 'contact_types_id': info_Person_contacts.contact_types_id,
                 'value': info_Person_contacts.value}
    return jsonify(dict_json)


@app.route('/person_contacts/<int:id>/delete')
def person_delete(id):
    info_Person = Person.query.get_or_404(id)
    info_Person_contacts = Person_contacts.query.get_or_404(id)
    db.session.delete(info_Person_contacts)
    db.session.commit()
    db.session.delete(info_Person)
    db.session.commit()
    return redirect('http://127.0.0.1:5000/all-users')


@app.route('/all-users/<int:id>/put',  methods=['PUT'])
def put_user(id):
    print("123")
    info_Person = Person.query.get_or_404(id)
    info_Person_contacts = Person_contacts.query.get_or_404(id)
    info_Person.first_name = request.json['first_name']
    print(info_Person.first_name)
    info_Person.second_name = request.json['second_name']
    info_Person.last_name = request.json['last_name']
    info_Person.first_name_genitive = request.json['first_name_genitive']
    info_Person.second_name_genitive = request.json['second_name_genitive']
    info_Person.mil_ranks_id = request.json['mil_ranks_id']
    info_Person.science_ranks_id = request.json['science_ranks_id']
    info_Person.science_levels_id = request.json['science_levels_id']
    info_Person.post_adress = request.json['post_adress']

    db.session.flush()

    info_Person_contacts.person_id = request.json['person_id']
    info_Person_contacts.contact_types_id = request.json['contact_types_id']
    info_Person_contacts.value = request.json['value']

    db.session.commit()


@app.route('/add_user', methods=['POST'])
def add_user():
    with app.app_context():
        first_name = request.json['first_name']
        second_name = request.json['second_name']
        last_name = request.json['last_name']
        first_name_genitive = request.json['first_name_genitive']
        second_name_genitive = request.json['second_name_genitive']
        mil_ranks_id = request.json['mil_ranks_id']
        science_ranks_id = request.json['science_ranks_id']
        science_levels_id = request.json['science_levels_id']
        post_adress = request.json['post_adress']

        person = Person(first_name=first_name, second_name=second_name, last_name=last_name,
                        first_name_genitive=first_name_genitive, second_name_genitive=second_name_genitive,
                        mil_ranks_id=mil_ranks_id, science_ranks_id=science_ranks_id,
                        science_levels_id=science_levels_id, post_adress=post_adress)

        db.session.add(person)
        db.session.flush()

        person_id = request.json['person_id']
        contact_types_id = request.json['contact_types_id']
        value = request.json['value']

        person_contacts = Person_contacts(person_id=person_id, contact_types_id=contact_types_id,
                                          value=value, Person_id=person.id)

        db.session.add(person_contacts)
        db.session.commit()


if __name__ == "__main__":
    app.run(port=5001, debug=True)