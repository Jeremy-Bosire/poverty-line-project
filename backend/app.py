from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import our models and database instance
from models import db

# This sets up the app and loads the configuration for our database.
app = Flask(__name__)

# Format: 'postgresql://<username>:<password>@<host>:<port>/<database>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:empty@localhost:5432/povertyline'

# This keeps things quiet; it prevents overhead tracking of every change.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# For session and security purposes. Store this in .env for production.
app.secret_key = 'dev-secret-key'

# Initialize the DB and Migrations
db.init_app(app)
migrate = Migrate(app, db)

# This is a simple landing route to test the server.
@app.route('/')
def index():
    return "Welcome to the Poverty Line Project!"

# These create the tables
with app.app_context():
    db.create_all()

# Run the Flask dev server (use gunicorn for production).
if __name__ == '__main__':
    # Turn on debug mode for dev; turn off in production
    app.run(debug=True)