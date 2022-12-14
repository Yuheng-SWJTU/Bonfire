# ///////////////////////////////////////////////////////////////////////////
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from logging.config import dictConfig
# ///////////////////////////////////////////////////////////////////////////

# init database
db = SQLAlchemy()

# init mail
mail = Mail()

# init auth
auth = HTTPBasicAuth()

# init api
api = Api()
