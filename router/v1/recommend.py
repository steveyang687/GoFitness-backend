from models.exercise import *
from flask import request, g
from libs.nestable_blueprint import NestableBlueprint
from flask_restful import Api, Resource
from libs.error_code import FormValidateException, ArgsTypeException
from models.user import UserProfile
from libs.response import generate_response
from serializer.user import user_schema
from libs.authorize import auth
import joblib
from sklearn.tree import DecisionTreeClassifier

raw = joblib.load("classifier/model.pkl")
classifier = raw['classifier']
transformer = raw['transform']
# usertype = classifier.predict([[0, 60, 160, 56]])[0]
sample = [[1,46,165.205127,70.944630]]
sample = transformer.transform(sample)
usertype = classifier.predict(sample)[0]


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
        weight = user.user_profile_weight
        height = user.user_profile_height
        age = user.user_profile_age
        sample = [[0, age, height, weight]]
        sample = transformer.transform(sample)
        user_type = classifier.predict(sample)[0]
        user_dict = user_schema.dump(user_type)

        return generate_response(data=user_dict)


api.add_resource(RecommendView, '/')