from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from manage import User

# import the blueprints
from views import main_blueprint
from auth import auth_blueprint

app = Flask(__name__)

# configuration settings
app.config['SECRET_KEY'] = 'asdfghjkl qwertyui'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# register the blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)

