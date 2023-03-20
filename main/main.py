from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from myprofile.myprofile import myProfile
from add_person.add_person import addPerson
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AlEx1902345@localhost/example_db'
db = SQLAlchemy(app)

app.register_blueprint(myProfile, url_prefix='/myprofile')
app.register_blueprint(addPerson, url_prefix='/add_person')


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/all-users')
def all_users():
    info = requests.get('http://127.0.0.1:5001')
    return render_template("all_users.html", articles=info.json())


@app.route('/all-users/<int:id>', methods=['GET'])
def get_user(id):
    info_Person = requests.get(f'http://127.0.0.1:5001/person/{id}')
    info_Person_contacts = requests.get(f'http://127.0.0.1:5001/person_contacts/{id}')
    return render_template("all_users_detail.html", info_Person=info_Person.json(),
                           info_Person_contacts=info_Person_contacts.json())


@app.route('/all-users/<int:id>/delete')
def del_user(id):
    requests.delete(f'http://127.0.0.1:5001/person/{id}/delete')
    return redirect('/all-users')


@app.route('/all-users/<int:id>/put', methods=['POST', 'GET'])
def put_user(id):
    info_Person = requests.get(f'http://127.0.0.1:5001/person/{id}')
    info_Person_contacts = requests.get(f'http://127.0.0.1:5001/person_contacts/{id}')
    if request.method == "POST":
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        last_name = request.form['last_name']
        first_name_genitive = request.form['first_name_genitive']
        second_name_genitive = request.form['second_name_genitive']
        mil_ranks_id = request.form['mil_ranks_id']
        science_ranks_id = request.form['science_ranks_id']
        science_levels_id = request.form['science_levels_id']
        post_adress = request.form['post_adress']
        person_id = request.form['person_id']
        contact_types_id = request.form['contact_types_id']
        value = request.form['value']
        requests.put(f'http://127.0.0.1:5001/all-users/{id}/put',
                     json={"first_name": first_name, "second_name": second_name,
                           "last_name": last_name,
                           "first_name_genitive": first_name_genitive,
                           "second_name_genitive": second_name_genitive,
                           "mil_ranks_id": mil_ranks_id,
                           "science_ranks_id": science_ranks_id,
                           "science_levels_id": science_levels_id,
                           "post_adress": post_adress, "person_id": person_id,
                           "contact_types_id": contact_types_id,
                           "value": value})
        return redirect('/all-users')
    else:
        return render_template("all_users_update.html", info_Person=info_Person.json(),
                               info_Person_contacts=info_Person_contacts.json())


if __name__ == "__main__":
    app.run(debug=True)
