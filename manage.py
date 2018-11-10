import unittest
from flask import Flask
import os
import coverage
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.api.v1.views import v1_blueprint
from app.api.v1.models import parcels
from app import *


# create the application object
app = Flask(__name__, instance_relative_config=True)

migrate = Migrate(app)
manager = Manager(app)

# config
app.config.from_object('instance.config.DevConfig')

# register blueprint
app.register_blueprint(v1_blueprint)


app.config.from_object('instance.config.DevConfig')


@manager.command
def test():
    """ runs the unit tests without coverage """
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    """ runs the unit tests without coverage """
    cov = coverage.coverage(
        branch=True,
        include='app/*'
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print("coverage summary")
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('instance.config.DevConfig')

    # register the blueprint
    app.register_blueprint(v1_blueprint)

    return app


if __name__ == '__main__':
    manager.run()
