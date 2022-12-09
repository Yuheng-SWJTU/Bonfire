from flask import Flask, g, session
from blueprints import user_bp, index_bp, camp_bp
import config
from flask_migrate import Migrate
from extensions import db, mail, api
from models import UserModel

# from flask_cors import CORS

app = Flask(__name__)
# CORS(app, supports_credentials=True)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
api.init_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(index_bp)
app.register_blueprint(camp_bp)


@app.before_request
def before_request():
    """
    This function will be executed before all requests.

    """

    # get user id from session
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # bind user to g
            g.user = user
        except:
            g.user = None


@app.context_processor
def context_processor():
    """
    This function will be executed before all templates.

    :return: user

    """

    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
