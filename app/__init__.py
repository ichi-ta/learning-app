from flask import Flask

app = Flask(__name__)

from app.src.logins.views import logins
from app.src.sets.views import sets

app.register_blueprint(logins)
app.register_blueprint(sets)