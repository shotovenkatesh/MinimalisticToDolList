import flask
from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask import Flask,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

# from wtforms import Form, StringField,SubmitField ,validators


app = Flask(__name__)
app.secret_key = "32-y8gfpbqu34nntcpgpr7924uhctqnwf8edh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


#db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500),  nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

#wtf form
class ToDoForm(FlaskForm):
    task = StringField("Add Task",validators=[DataRequired()])
    submit = SubmitField()



# all_tasks = []
@app.route("/",methods=['GET', 'POST'])
def home():
    data_from_db = db.session.query(User).all()
    form = ToDoForm()
    if flask.request.method == "POST":
        user_task = flask.request.values.get("task")
        new_task = User(
            task = user_task
        )
        db.session.add(new_task)
        db.session.commit()
        data_from_db = db.session.query(User).all()


    return render_template("index.html",form=form,tasks = data_from_db)

@app.route("/del",methods = ["GET","POST"])
def delete_task():
    task_id = request.args.get("id")
    task_to_delete = User.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)