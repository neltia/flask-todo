#Call Lib
from flask import Flask, render_template,request,redirect,url_for
from pymongo import MongoClient
from bson import ObjectId 
from datetime import datetime

#Config setting
app = Flask(__name__)
connection = MongoClient('localhost', 27017) #ip, port
db = connection.project
todos = db.todo

#Error Process
@app.errorhandler(404)
def page_not_found(error):
	app.logger.error(error)
	return render_template('page_not.html'), 404

#home
@app.route("/")
@app.route("/about")
def home_page():
	return render_template('about.html')

#All list page
@app.route("/all")
def all_page():
	todolist = todos.find()
	stat = "All list"
	return render_template('index.html', todos=todolist, stat=stat)

#Active item list
@app.route("/active")
def active_page():
	todolist = todos.find({"done":"no"})
	stat = "Active list"
	return render_template('index.html', todos=todolist, stat=stat)

#Completed item list
@app.route("/completed")
def complete_page():
	todolist = todos.find({"done":"yes"})
	stat = "Completed list"
	return render_template('index.html', todos=todolist, stat=stat)

#Update memo
@app.route("/update")
def update_page():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task)

#New memo
@app.route("/action", methods=['GET','POST'])
def action_add():
	if request.method == 'POST':
		contents = request.values.get('contents')
		date = datetime.today()
		primary = request.values.get('primary')
		todos.insert_one({"contents":contents, "date":date, "primary":primary, "done":"no"})
		todos.delete_many({"contents":{"$eq": ""}})
		return redirect(url_for('all_page'))
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
	return redirect(url_for('all_page'))

#Delete memo
@app.route("/delete")
def action_delete():
	key=request.values.get("_id")
	todos.delete_one({"_id":ObjectId(key)})
	return redirect(url_for('all_page'))

#Done memo update
@app.route("/action2", methods=['GET','POST'])
def done_update():
	if request.method == 'POST':
		id=request.values.get("_id")
		contents = request.values.get('contents')
		primary = request.values.get('primary')
		todos.update_one({"_id":ObjectId(id)}, {'$set':{"contents":contents, "primary":primary}})
		todos.delete_many({"contents":{"$eq": ""}})
		return redirect(url_for('all_page'))
	else:
		return render_template('page_not.html')

if __name__ == "__main__":    
    app.run(debug=True)