from faker import Faker
import random

from sqlalchemy.exc import IntegrityError

from models.exercise import *

fake = Faker()

length = ["11'20\"", "19'20\"", "15'12\""]
category = ["HIIT", "Jogging", "Swimming", "Running"]
purpose = ["lose weight", "keep fit", "muscle"]
intensity = ["low", "medium", "high"]
video_type = [i for i in range(10)]

def fake_category(count=4):
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_purpose(count=3):
    for i in range(count):
        purpose_temp = Purpose(name=purpose[i])
        db.session.add(purpose_temp)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_intensity(count=3):
    for i in range(count):
        intensity_temp = Intensity(name=intensity[i])
        db.session.add(intensity_temp)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_video_type(count=10):
    for i in range(count):
        video_type_temp = VideoType(name=str(video_type[i]))
        db.session.add(video_type_temp)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_exercise(count=50):
    for i in range(count):
        exercise = Exercise(
            exercise_name=fake.word(),
            exercise_length=random.choice(length),
            video_link="http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4",
            description=fake.text(200),
            category_id=random.randint(1, Category.query.count()),
            image_url="http://goodpic.jpg",
            intensity_id=random.randint(1, Intensity.query.count()),
            purpose_id=random.randint(1, Purpose.query.count()),
            video_type_id=random.randint(1, VideoType.query.count()),
        )
        db.session.add(exercise)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

if __name__ == '__main__':
    fake_category()
    fake_exercise()