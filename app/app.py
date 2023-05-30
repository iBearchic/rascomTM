from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from manage import db, User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    from views import main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

if __name__ == "__main__":
    app = create_app()
    # with app.app_context():
    #     db.create_all()
    app.run()


