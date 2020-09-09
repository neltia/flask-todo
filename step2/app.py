#Call Lib
from flask import Flask
from flask import render_template

#Config setting
app = Flask(__name__)

#home
@app.route("/")
@app.route("/about")
def home_page():
	return render_template('about.html')

if __name__ == "__main__":
    app.run()