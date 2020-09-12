#Call Lib
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from pymongo import MongoClient
from bson import ObjectId 
from datetime import datetime

class TextForm(FlaskForm):
    content = StringField('내용', validators=[DataRequired()])

#Config setting
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
connection = MongoClient('localhost', 27017) #ip, port
db = connection.project
todos = db.todo

#Error Process
@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not.html'), 404

#home
@app.route("/")
@app.route("/about")
def home_page():
	return render_template('about.html')

#All list page
@app.route("/all")
def all_page():
	stat = "All list"
	todolist = todos.find().sort('date',-1)
	form = TextForm()
	return render_template('index.html', todos=todolist, stat=stat, form=form)

#Active item list
@app.route("/active")
def active_page():
	stat = "Active list"
	todolist = todos.find({"done":"no"}).sort('date',-1)
	form = TextForm()
	return render_template('index.html', todos=todolist, stat=stat, form=form)

#Completed item list
@app.route("/completed")
def complete_page():
	stat = "Completed list"
	todolist = todos.find({"done":"yes"}).sort('date',-1)
	form = TextForm()
	return render_template('index.html', todos=todolist, stat=stat, form=form)

#Update memo
@app.route("/update")
def update_page():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})[0]
	form = TextForm()
	return render_template('update.html', task=task, form=form)

#New memo
@app.route("/action", methods=['GET','POST'])
def action_add():
	form = TextForm()
	if form.validate_on_submit():
		contents = request.form['content']
		date = datetime.today()
		primary = request.values.get('primary')
		todos.insert_one({"contents":contents, "date":date, "primary":primary, "done":"no"})
		return """<script>
			window.location = document.referrer;
			</script>"""
	else:
		return render_template('page_not.html')

#Done memo change
@app.route("/done")
def done_add():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	return """<script>
		window.location = document.referrer;
		</script>"""

#Delete memo
@app.route("/delete")
def action_delete():
	key=request.values.get("_id")
	todos.delete_one({"_id":ObjectId(key)})
	return """<script>
		window.location = document.referrer;
		</script>"""

#Done memo update
@app.route("/action2", methods=['GET','POST'])
def done_update():
	if request.method == 'POST':
		key = request.values.get("_id")
		contents = request.form['content']
		primary = request.values.get('primary')
		todos.update_one({"_id":ObjectId(key)}, {'$set':{"contents":contents, "primary":primary}})
		return redirect(url_for('all_page'))
	else:
		return render_template("page_not.html")

if __name__ == "__main__":
    app.run()