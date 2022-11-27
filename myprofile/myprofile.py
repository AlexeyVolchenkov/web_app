from flask import Blueprint, render_template, url_for, request, redirect

myProfile = Blueprint('myprofile', __name__, template_folder='templates', static_folder='static')

@myProfile.route('/', methods=['POST', 'GET'])
def myprofile():
    if request.method == "POST":
        name = request.form['name']
        try:
            return redirect(f'/myprofile/{name}')
        except:
            return "При добавлении информации о пользователе произошла ошибка"
    else:
        return render_template("myprofile/myProfile.html")

@myProfile.route('/<name>')
def myprofile1(name):
    name = name
    return render_template("myprofile/myProfile1.html", articles=name)