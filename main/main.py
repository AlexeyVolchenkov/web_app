from flask import Flask, render_template, url_for, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from myprofile.myprofile import myProfile
from add_person.add_person import addPerson
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AlEx1902345@localhost/example_db'
db = SQLAlchemy(app)

app.register_blueprint(myProfile, url_prefix='/myprofile')
app.register_blueprint(addPerson, url_prefix='/add_person')


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
def main():
    return render_template("main.html")


@app.route('/all-users')
def all_users():
    info = Person.query.order_by(Person.id).all()
    return render_template("all_users.html", articles=info)


if __name__ == "__main__":
    app.run(debug=True)