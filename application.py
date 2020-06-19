from flask import Flask, render_template

from wtForm import * # this is a local import 
from models import * # this is a local import

# Config App
app = Flask(__name__)
app.secret_key = 'replace later'

#config db
app.config['SQLALCHEMY_DATABASE_URI']='postgres://abnmpaqprcrhne:07e59ceaec54185c8c85ee04be039025810164a07403aad83053c7be2b278066@ec2-54-161-208-31.compute-1.amazonaws.com:5432/d9ue9spbrno6dt'

db = SQLAlchemy(app)

@app.route('/', methods=['GET','POST'])
def index():

    reg_form = RegistartionForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data


        # check username exits
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has taken this username"
        
        #add user to db
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into db"



    return render_template("index.html", form=reg_form)

if __name__ == "__main__":
    app.run(debug=True)