from .v1 import v1_bp


def init_app(app):
    # app核心对象
    app.register_blueprint(v1_bp)