from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

import views