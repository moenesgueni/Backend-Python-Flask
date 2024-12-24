from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from routes import books


app = Flask(__name__)
api = Api(app)

# Load configurations from the config file
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database is created
    app.run(debug=True)
