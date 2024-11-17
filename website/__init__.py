from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import datetime

db = SQLAlchemy()
DB_NAME = "database.db"





def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

    from .views import views
    from .auth import auth
    from .threads import thread


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(thread, url_prefix='/')

    def time_ago(timestamp):
        """Calculate how long ago a timestamp occurred."""
        now = datetime.utcnow()
        delta = now - timestamp

        if delta.days > 1:
            return f"{delta.days} days ago"
        elif delta.days == 1:
            return "1 day ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} hours ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"

    # Register the filter in Jinja2
    app.jinja_env.filters['timeago'] = time_ago


    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
