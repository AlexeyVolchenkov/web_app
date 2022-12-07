from flask import Blueprint, render_template, url_for, request, redirect

addPerson = Blueprint('add_person', __name__, template_folder='templates', static_folder='static')


@addPerson.route('/', methods=['POST', 'GET'])
def create_user():
    from main import Person, db, app, Person_contacts
    if request.method == "POST":
        with app.app_context():
            first_name = request.form['first_name']
            second_name = request.form['second_name']
            last_name = request.form['last_name']
            first_name_genitive = request.form['first_name_genitive']
            second_name_genitive = request.form['second_name_genitive']
            mil_ranks_id = request.form['mil_ranks_id']
            science_ranks_id = request.form['science_ranks_id']
            science_levels_id = request.form['science_levels_id']
            post_adress = request.form['post_adress']

            person = Person(first_name=first_name, second_name=second_name, last_name=last_name,
                            first_name_genitive=first_name_genitive, second_name_genitive=second_name_genitive,
                            mil_ranks_id=mil_ranks_id, science_ranks_id=science_ranks_id,
                            science_levels_id=science_levels_id, post_adress=post_adress)

            db.session.add(person)
            db.session.flush()

            person_id = request.form['person_id']
            contact_types_id = request.form['contact_types_id']
            value = request.form['value']

            person_contacts = Person_contacts(person_id=person_id, contact_types_id=contact_types_id,
                                              value=value, Person_id=person.id)

            db.session.add(person_contacts)
            db.session.commit()
        return redirect('/all-users')
        db.session.rollback()
        return "Ошибка добавления в базу данных"
    else:
        return render_template("add_person/myProfile.html")