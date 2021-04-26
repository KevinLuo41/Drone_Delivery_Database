from flask import Flask, render_template, request, Response, g
from datetime import timedelta
import sqlite3
from flaskext.mysql import MySQL
from backend import backend_api, db

DATABASE = './drone_.db'

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'TEAM39'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
db.init_app(app)

app.register_blueprint(backend_api)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/admin_home', methods=['GET','POST'])
def admin_home():
    return render_template("admin_home.html")

@app.route('/create_chain', methods=['GET','POST'])
def create_chain():
    return render_template("create_chain.html")

@app.route('/create_store', methods=['GET','POST'])
def create_store():
    return render_template("create_store.html")




if __name__ == '__main__':
    app.run(debug=True)