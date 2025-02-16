from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


# Create an instance of a class flask
app = Flask(__name__)
CORS(app, resources={
    r"/upload-ics": {"origins": "*"},
    r"/events": {"origins": "*"},
    r"/add_events": {"origins": "*"},
    r"/login": {"origins": "*"}
}, supports_credentials=True)

# SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database URI
app.config["SECRET_KEY"] = "##Secret Key##"




db = SQLAlchemy(app) # Initialize the database object
login_manager = LoginManager(app) # login manager which handles all the sessions and cookies
login_manager.login_view = 'login'
 


UPLOAD_FOLDER = "uploads" # Folder to store uploaded files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create uploads folder if not exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER # Set the upload folder in the app configuration

from . import routes
