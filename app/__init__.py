from flask import Flask
# we import created blueprints to register them
from .api.v1.views import v1_blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('instance.config.DevConfig')

    # register the blueprint
    app.register_blueprint(v1_blueprint)

    return app
