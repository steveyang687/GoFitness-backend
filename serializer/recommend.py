from .base import ma
from models.exercise import Exercise, Category, ExerciseImage


class RecommendSchema(ma.Schema):
    class Meta:
        model = Exercise
        fields = ('exercise_name', 'exercise_length', 'description')


reco_schema = RecommendSchema()
