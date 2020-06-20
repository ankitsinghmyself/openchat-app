from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user,current_user,login_required,logout_user

from wtForm import * # this is a local import 
from models import * # this is a local import


# Config App
app = Flask(__name__)
app.secret_key = 'replace later'

#config db
app.config['SQLALCHEMY_DATABASE_URI']='postgres://abnmpaqprcrhne:07e59ceaec54185c8c85ee04be039025810164a07403aad83053c7be2b278066@ec2-54-161-208-31.compute-1.amazonaws.com:5432/d9ue9spbrno6dt'

db = SQLAlchemy(app)

#config flask login
login = LoginManager(app)
login.init_app(app)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET','POST'])
def index():

    #update db if validation success
    reg_form = RegistartionForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        #hash pswd
        hash_pswd = pbkdf2_sha256.hash(password)
        #add user to db
        user = User(username=username, password=hash_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # allow login if validation success
    if login_form.validate_on_submit():
        user_object=User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        # if current_user.is_authenticated:
        #     return "flsk logged in"
        return redirect(url_for('openchat'))

    return render_template("login.html", form=login_form)

@app.route('/openchat', methods=['GET','POST'])
# @login_required
def openchat():
    if not current_user.is_authenticated:
            return "Please login before chat"

    return "user login in chat"

@app.route('/logout', methods=['GET'])
def logout():

    logout_user()
    return "logedout"
    

if __name__ == "__main__":
    app.run(debug=True)