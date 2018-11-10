from flask import Flask
from app.api.v1.views import v1_blueprint
from app.api.v1.models import parcels

# create the application object
app = Flask(__name__, instance_relative_config=True)

# config
app.config.from_object('instance.config.DevConfig')

# register blueprint
app.register_blueprint(v1_blueprint)


app.config.from_object('instance.config.DevConfig')


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('instance.config.DevConfig')

    # register the blueprint
    app.register_blueprint(v1_blueprint)

    return app
