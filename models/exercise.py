from .base import db


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    exercises = db.relationship('Exercise', backref='category')  # 目前每种运动只支持一种category


class Exercise(db.Model):
    __tablename__ = "exercise"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_name = db.Column(db.String(100), nullable=False, unique=True)
    exercise_length = db.Column(db.Integer, nullable=False)  # in minutes
    description = db.Column(db.String(256))
    exercise_link = db.Column(db.String(256))  # 视频
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class ExerciseImage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    image_url = db.Column(db.String(256))
