from .base import db


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    exercises = db.relationship('Exercise', backref='category')  # 目前每种运动只支持一种category: HIIT...


class Exercise(db.Model):
    __tablename__ = "exercise"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_name = db.Column(db.String(100), nullable=False, unique=True)
    exercise_length = db.Column(db.String(50), nullable=False)  # in minutes
    description = db.Column(db.String(256))
    video_link = db.Column(db.String(256))  # 视频
    image_url = db.Column(db.String(256))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    purpose_id = db.Column(db.Integer, db.ForeignKey('purpose.id'))
    intensity_id = db.Column(db.Integer, db.ForeignKey('intensity.id'))
    video_type_id = db.Column(db.Integer, db.ForeignKey('video_type.id'))


class Purpose(db.Model):
    __tablename__ = "purpose"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    exercise = db.relationship('Exercise', backref='purpose')


class Intensity(db.Model):
    __tablename__ = "intensity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    exercise = db.relationship('Exercise', backref='intensity')


class VideoType(db.Model):
    __tablename__ = "video_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    exercise = db.relationship('Exercise', backref='video_type')