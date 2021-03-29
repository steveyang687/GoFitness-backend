from models.exercise import Exercise, Category, ExerciseImage
from libs.nestable_blueprint import NestableBlueprint

recommend_bp = NestableBlueprint('reco_v1', __name__, url_prefix='recommend/')
