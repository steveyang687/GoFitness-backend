from models.exercise import *
from flask import request, g
from libs.nestable_blueprint import NestableBlueprint
from flask_restful import Api, Resource
from libs.error_code import FormValidateException, ArgsTypeException
from models.user import UserProfile
from libs.response import generate_response
from serializer.user import user_schema
from serializer.recommend import reco_schema
from libs.authorize import auth
import joblib
from sklearn.tree import DecisionTreeClassifier

raw = joblib.load("classifier/model.pkl")
classifier = raw['classifier']
transformer = raw['transform']
# sample = [[1,46,165.205127,70.944630]]
# sample = transformer.transform(sample)
# usertype = classifier.predict(sample)[0]


recommend_bp = NestableBlueprint('reco_v1', __name__, url_prefix='recommend/')

api = Api(recommend_bp)


class RecommendView(Resource):
    def post(self):
        data = request.json
        if not data:
            raise ArgsTypeException(message="传参的方式不对，或没有传参")

    # @auth.login_required
    def get(self):
        """获取用户，并返回用户信息"""
        # user = UserProfile.query.get(g.user["uid"])
        data = request.json
        user_name = data['user_name']
        user = UserProfile.query.filter_by(user_profile_name=user_name).limit(1)[0]
        weight = user.user_profile_weight
        height = user.user_profile_height
        age = user.user_profile_age
        sample = [[0, age, height, weight]]
        sample = transformer.transform(sample)
        user_type = classifier.predict(sample)[0]

        videos = Exercise.query.filter_by(video_type_id=user_type).limit(3)
        recommends = {'user_type': user_type}
        temp = {}
        for i in range(3):
            temp[i] = {
                'exercise_name': videos[i].exercise_name,
                'exercise_length': videos[i].exercise_length,
                'description': videos[i].description,
                'video_link': videos[i].video_link,
                'image_url': videos[i].image_url,
                'category_id': videos[i].category_id
            }
        recommends['recommend'] = temp
        # reco_dict = reco_schema.dump(recommends)

        return generate_response(data=recommends)


api.add_resource(RecommendView, '/')