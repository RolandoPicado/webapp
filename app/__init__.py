from flask import Flask
from flask_login import LoginManager
from .models import db, User
from .routes import main #Für 'main' blueprint von routes.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://aero_user:dbuser@localhost/aero_festival'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'e@&kHYEq*%4a(#J'  # Change this to a random secret key!
    
    #enable auto-reloading
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Initialize the database
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

   

    # Set up Flask-Login
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main)

    return app
