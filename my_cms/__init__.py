import os

from dotenv import load_dotenv

from flask import Flask


def create_app(test_config=None):

    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'), DATABASE=os.path.join(app.instance_path, os.getenv('DATABASE'))
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)

    else:
        app.config.from_mapping(test_config)

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import blog

    app.register_blueprint(blog.bp)

    from . import projects

    app.register_blueprint(projects.bp)

    from . import index
    app.register_blueprint(index.bp)

    from . import account
    app.register_blueprint(account.bp)

    return app
