from time import localtime, strftime
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user,current_user,login_required,logout_user
from flask_socketio import SocketIO,send,emit, join_room, leave_room
import os
from wtForm import * # this is a local import 
from models import * # this is a local import


# Config App
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')
#app.secret_key = 'SECRET'
#config db
#app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI']='postgres://abnmpaqprcrhne:07e59ceaec54185c8c85ee04be039025810164a07403aad83053c7be2b278066@ec2-54-161-208-31.compute-1.amazonaws.com:5432/d9ue9spbrno6dt'
db = SQLAlchemy(app)

rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))

#Initialize Flas-SockectIO
socketio = SocketIO(app)
socketio.init_app(app)
ROOMS=["General","news","games","coding"]

#config flask login
login = LoginManager(app)
login.init_app(app)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET','POST'])
def index():
    template_path=rel('templates')
    static_path=rel('static')

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
        flash("Registered successfully. Please login.","success")
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
        flash("Please login.","danger")
        return redirect(url_for('login'))

    return render_template('openchat.html', username = current_user.username, rooms=ROOMS)

@app.route('/logout', methods=['GET'])
def logout():

    logout_user()
    flash("You have successfully logout.","success")
    return redirect(url_for('login'))
    
@socketio.on('message')
def message(data):
    #print(f"\n\n{data}\n\n")
    #print(f"\n\n\n\n{current_user.username}\n\n\n\n")
    send({'msg': data['msg'], 'username': data['username'],'time_stamp': datetime.now().strftime('%b-%d %I:%M%p')}, room=data['room'])
    #print(f"\n\n\n\n\n\n{current_user.username}\n\n\n\n")

@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({ 'msg': data['username'] + " has joined the "
    + data['room'] + " room" }, room=data['room'])

@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({ 'msg': data['username'] + "has left the "
    + data['room'] + "room" }, room=data['room'])

if __name__ == "__main__":
    #socketio.run(app, debug=True)
    app.run()