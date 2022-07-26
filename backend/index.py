from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from models.tables import db
from routes.filter_bp import filter_bp
from routes.file_bp import file_bp

app = Flask(__name__)
app.config.from_object("config")

# CORS implemented so that we don't get errors when trying to access the server from a different server location
CORS(app)


try:
    db.init_app(app)

    app.register_blueprint(filter_bp, url_prefix="/filter")
    app.register_blueprint(file_bp, url_prefix="/file")

except:
    print("Error")
