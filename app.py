import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from models.fakes import *
import click


def create_app(config=None):
    app = Flask(__name__)
    # 配置跨域资源共享
    cors = CORS(app, resources={'*': {'origins': '*'}})

    # load default configuration
    app.config.from_object('config.settings')
    # app.config.from_object('config.secure')

    # load environment configuration
    # FLASK_CONF="/path/to/config_dev.py"
    # FLASK_CONF="/path/to/config_prod.py"
    # 也可以根据系统环境变量，加载不同的配置文件
    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    app.app_context().push()
    import router
    import models
    import serializer
    router.init_app(app)
    serializer.init_app(app)
    models.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Register cli commands
    register_commands(app)
    return app


def register_commands(app):

    @app.cli.command()
    @click.option('--category_num', default=4, help='Quantity of categories, default is 10')
    @click.option('--exercise_num', default=50, help='Quantity of exercises, default is 50')
    def forge(category_num, exercise_num):
        """Generate Fake Exercise Data"""
        db.drop_all()
        db.create_all()
        click.echo('Generating %d categories...' % category_num)
        fake_category(category_num)
        fake_purpose(3)
        fake_intensity(3)
        fake_video_type(10)
        click.echo('Generating %d exercises...' % exercise_num)
        fake_exercise(exercise_num)

        click.echo('Done.')
