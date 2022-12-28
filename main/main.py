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


@app.route('/all-users/<int:id>', methods=['GET'])
def get_user(id):
    info_Person = Person.query.get(id)
    info_Person_contacts = Person_contacts.query.get(id)
    return render_template("all_users_detail.html", info_Person=info_Person, info_Person_contacts=info_Person_contacts)


@app.route('/all-users/<int:id>/delete')
def del_user(id):
    info_Person = Person.query.get_or_404(id)
    info_Person_contacts = Person_contacts.query.get_or_404(id)
    db.session.delete(info_Person_contacts)
    db.session.commit()
    db.session.delete(info_Person)
    db.session.commit()
    return redirect('/all-users')


@app.route('/all-users/<int:id>/put',  methods=['POST', 'GET'])
def put_user(id):
    info_Person = Person.query.get_or_404(id)
    info_Person_contacts = Person_contacts.query.get_or_404(id)
    if request.method == "POST":
        info_Person.first_name = request.form['first_name']
        info_Person.second_name = request.form['second_name']
        info_Person.last_name = request.form['last_name']
        info_Person.first_name_genitive = request.form['first_name_genitive']
        info_Person.second_name_genitive = request.form['second_name_genitive']
        info_Person.mil_ranks_id = request.form['mil_ranks_id']
        info_Person.science_ranks_id = request.form['science_ranks_id']
        info_Person.science_levels_id = request.form['science_levels_id']
        info_Person.post_adress = request.form['post_adress']

        db.session.flush()

        info_Person_contacts.person_id = request.form['person_id']
        info_Person_contacts.contact_types_id = request.form['contact_types_id']
        info_Person_contacts.value = request.form['value']

        db.session.commit()
        return redirect('/all-users')
    else:
        return render_template("all_users_update.html", info_Person=info_Person, info_Person_contacts=info_Person_contacts)


if __name__ == "__main__":
    app.run(debug=True)