from flask import Flask

app = Flask(__name__)

#from app.src.users.views import users
from app.src.logins.views import logins

#app.register_blueprint(users)
app.register_blueprint(logins)