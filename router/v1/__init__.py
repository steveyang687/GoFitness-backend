from libs.nestable_blueprint import NestableBlueprint
from .user import user_bp

v1_bp = NestableBlueprint('v1', __name__, url_prefix='/v1/api/')

v1_bp.register_blueprint(user_bp)
