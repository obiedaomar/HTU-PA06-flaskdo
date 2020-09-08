import os

from flask import Flask, session, render_template


def create_app(test_config=None):
    # create the Flask
    app = Flask(__name__, instance_relative_config=True)

    # configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskdo.sqlite'),
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 403 error handler
    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('errors/403.html'), 403

    # 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    # 500 error handler
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # register template global function
    @app.template_global()
    def is_logged_in():
        if 'uid' in session:
            return True
        return False

    # import helper DB functions
    from . import db
    db.init_app(app)

    # TODO: Register your blueprints here :).
    from .views import login
    app.register_blueprint(login.bp)

    from .views import index
    app.register_blueprint(index.bp)

    from .views import task_list
    app.register_blueprint(task_list.bp)

    from .views import task
    app.register_blueprint(task.bp)

    return app
