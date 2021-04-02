from .base import ma
from models.exercise import *


class RecommendSchema(ma.Schema):
    class Meta:
        model = Exercise
        fields = ('exercise_name', 'exercise_length', 'description', 'video_link', 'image_url', 'category_id')


reco_schema = RecommendSchema()
