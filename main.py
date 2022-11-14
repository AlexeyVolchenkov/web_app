from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Information(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Information %r>' % self.id+


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/all-users')
def all_users():
    info = Information.query.order_by(Information.id).all()
    return render_template("all_users.html", articles=info)


@app.route('/create-user', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        address = request.form['address']

        user = Information(name=name, surname=surname, phone=phone, address=address)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/all-users')
        except:
            return "При добавлении информации о пользователе произошла ошибка"
    else:
        return render_template("create-user.html")


if __name__ == "__main__":
    app.run(debug=True)