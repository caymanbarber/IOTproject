import os

from flask import Flask


def create_app(test_config=None)->Flask:
    """Create, init, and return flask application with pages
    
    Keyword arguments:
    test_config -- config file for testing
    Return: Flask app
    """
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  #change after development
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Database 
    from . import db
    db.init_app(app)

    #Authorization
    from . import auth
    app.register_blueprint(auth.bp)

    #Graph and Data Visualization
    from . import dataVisualizer
    app.register_blueprint(dataVisualizer.bp)
    app.add_url_rule('/', endpoint='index')

    # Device and Sensor Management and Registration
    from . import deviceRegistration
    app.register_blueprint(deviceRegistration.bp)

    return app

    




