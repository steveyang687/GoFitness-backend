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
from numpy.random import choice
from sklearn.tree import DecisionTreeClassifier

raw = joblib.load("classifier/model.pkl")
classifier = raw['classifier']
transformer = raw['transform']
# sample = [[1,46,165.205127,70.944630]]
# sample = transformer.transform(sample)
# usertype = classifier.predict(sample)[0]

user_ex_mapping = {1: [1, 7, 13, 19],
                   2: [5, 11, 17, 23],
                   3: [3, 9, 15, 21],
                   4: [2, 8, 14, 20],
                   5: [5, 6, 11, 12, 17, 18, 23, 24],
                   6: [4, 10, 16, 22]
                   }

full_type_list = [i for i in range(1, 25)]

recommend_bp = NestableBlueprint('reco_v1', __name__, url_prefix='recommend/')

api = Api(recommend_bp)


class RecommendView(Resource):
    # def post(self):
    #     data = request.json
    #     if not data:
    #         raise ArgsTypeException(message="传参的方式不对，或没有传参")

    # @auth.login_required
    def post(self):
        """获取用户，并返回用户信息"""
        # user = UserProfile.query.get(g.user["uid"])
        data = request.json
        user_name = data['user_name']
        user = UserProfile.query.filter_by(user_profile_name=user_name).first()
        weight = user.user_profile_weight
        height = user.user_profile_height
        age = user.user_profile_age
        sample = [[1, age, height, weight]]
        sample = transformer.transform(sample)
        user_type = classifier.predict(sample)[0]

        prefer = [user.prefer_1,
                  user.prefer_2,
                  user.prefer_3,
                  user.prefer_4,
                  ]

        # videos = Exercise.query.filter(Exercise.video_type_id.in_(user_ex_mapping[user_type])).all()

        recommends = {'user_type': user_type}
        random_pick = list(choice(user_ex_mapping[user_type], size=4, replace=False))
        temp = {}
        i = 0
        other_prob = list(set(full_type_list).difference(set(user_ex_mapping[user_type])))
        random_pick.extend(choice(other_prob, 1))
        for video_type in random_pick:
            video_list = []
            videos = Exercise.query.filter(Exercise.video_type_id == video_type)\
                .order_by(Exercise.advertise_charge.desc()).all()
            if video_type in prefer:
                video_list.extend(choice(videos, 2))
            else:
                video_list.extend(choice(videos, 1))
            for video in video_list:
                temp["re" + str(i)] = {
                    'exercise_name': video.exercise_name,
                    'exercise_length': video.exercise_length,
                    'description': video.description,
                    'video_link': video.video_link,
                    'image_url': video.image_url,
                    'category': Category.query.get(video.category_id).name
                }
                i += 1
            if i == 6:
                break
        recommends['recommend'] = temp
        # reco_dict = reco_schema.dump(recommends)

        return generate_response(data=recommends)


api.add_resource(RecommendView, '/')
