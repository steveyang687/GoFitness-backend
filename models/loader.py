from .base import db
import csv
from sqlalchemy.exc import IntegrityError
from models.exercise import *

category_dict = ["HIIT", "Zumba", "Yoga", "Boxing"]
purpose_dict = {1: "lose fat", 2: "muscle", 3: "keep fit"}
intensity_dict = {1: "high", 0: "low"}


def generate_helping_tables():
    for key, value in purpose_dict.items():
        purpose = Purpose(no=key, name=value)
        db.session.add(purpose)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    for key in category_dict:
        category = Category(name=key)
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    for key, value in intensity_dict.items():
        intensity = Intensity(no=key, name=value)
        db.session.add(intensity)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    for key in range(1, 25):
        video = VideoType(name=str(key))
        db.session.add(video)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def data_load(path="../videodata.csv"):
    with open(path, encoding='utf-8')as f:
        f_csv = csv.reader(f)
        flag = 0
        for row in f_csv:
            if flag == 0 or row[0] == '':
                flag = 1
                continue
            # print(row)
            exercise = Exercise(video_type_id=int(row[1]),
                                category_id=Category.query.filter_by(name=row[2]).one().id,
                                purpose_id=Purpose.query.filter_by(name=purpose_dict[int(row[3])]).one().id,
                                intensity_id=Intensity.query.filter_by(name=intensity_dict[int(row[4])]).one().id,
                                exercise_name=row[5],
                                description=row[6],
                                image_url=row[7],
                                video_link=row[8],
                                exercise_length=row[9],
                                advertise_charge=float(row[10]),
                                )
            db.session.add(exercise)
            # db.session.commit()
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


# data_load()