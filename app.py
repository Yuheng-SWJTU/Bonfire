from flask import Flask
from blueprints import user_bp, index_bp, camp_bp
import config
from flask_migrate import Migrate
from extensions import db, mail, api
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

if __name__ == '__main__':
    app.run()
