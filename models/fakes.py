from faker import Faker
import random

from sqlalchemy.exc import IntegrityError

from models.exercise import *

fake = Faker()


def fake_category(count=10):
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_exercise(count=50):
    for i in range(count):
        exercise = Exercise(
            exercise_name=fake.word(),
            exercise_length=random.randint(10, 50),
            exercise_link="http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4",
            description=fake.text(200),
            category_id=random.randint(1, Category.query.count())
        )
        db.session.add(exercise)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        exercise_image = ExerciseImage(
            exercise=exercise.id,
            image_url="https://imgtu.com/i/cS2PfS"
        )
        db.session.add(exercise_image)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

if __name__ == '__main__':
    fake_category()
    fake_exercise()