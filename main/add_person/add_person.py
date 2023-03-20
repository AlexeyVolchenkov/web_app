from flask import Blueprint, render_template, url_for, request, redirect
import requests

addPerson = Blueprint('add_person', __name__, template_folder='templates', static_folder='static')


@addPerson.route('/', methods=['POST', 'GET'])
def create_user():
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

        requests.post('http://127.0.0.1:5001/add_user', json={"first_name": first_name, "second_name": second_name,
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
        return render_template("add_person/myProfile.html")
