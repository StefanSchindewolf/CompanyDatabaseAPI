# Import Modules
import os
import sys
import sqlite3
import logging
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s \t %(message)s ',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
)
log = logging.getLogger('log')

# Set application directory to current execution dir
basedir = os.path.abspath(os.path.dirname(__file__))

# Connexion application instance for connecting to DB
connex_app = connexion.App(__name__, specification_dir=basedir)

# Flask app instance for REST server interface
app = connex_app.app

# SQLAlchemy as part of application to abstract db implementation from REST
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'company.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy database instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

