# This __init__.py file will hold code for our Flask factory function, which is a function we use to set and create the Flask application instance where you link all your Flask blueprints together. Think of the factory function as the central function in which all our Flask components (blueprints) are combined into one application and that you can use to create different Flask application instances for different purposes with different configurations. For example, you could use the factory function to create a Flask application instance for testing with proper configurations for testing.

from flask import Flask
from flask_login import LoginManager
from config import Config
from app.extensions import db

def create_app(config_class = Config):
    '''Flask application factory function (https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/)'''

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Specify the user loader which tells flask-login how to find a specific user from the ID that is stored in their session cookie
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix = '/auth')

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix = '/posts')
  
    return app