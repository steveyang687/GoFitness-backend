from models.exercise import Exercise, Category, ExerciseImage
from flask import request, g
from libs.nestable_blueprint import NestableBlueprint
from flask_restful import Api, Resource
from libs.error_code import FormValidateException, ArgsTypeException
from models.user import UserProfile
from libs.response import generate_response
from serializer.user import user_schema
from libs.authorize import auth
recommend_bp = NestableBlueprint('reco_v1', __name__, url_prefix='recommend/')

api = Api(recommend_bp)

class RecommendView(Resource):
    def post(self):
        data = request.json
        if not data:
            raise ArgsTypeException(message="传参的方式不对，或没有传参")

    @auth.login_required
    def get(self):
        """获取用户，并返回用户信息"""
        user = UserProfile.query.get(g.user["uid"])
        user_dict = user_schema.dump(user)
        user_dict[
            "avatar"] = "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1016301861,2773103463&fm=26&gp=0.jpg"

        return generate_response(data=user_dict)


api.add_resource(RecommendView, '/')