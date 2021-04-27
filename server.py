from flask import Flask
from datetime import timedelta
from backend import backend_api, db
from frontend import frontend_api


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kevin112911/'
app.config['MYSQL_DATABASE_DB'] = 'grocery_drone_delivery'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
db.init_app(app)

app.register_blueprint(backend_api)
app.register_blueprint(frontend_api)

if __name__ == '__main__':
    app.run(debug=True)