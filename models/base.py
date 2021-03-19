from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
# from flask import Flask

# app = Flask(__name__)
# app.config['SQLALCHEMY_DARABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/gofitness'

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/gofitness'
# db = SQLAlchemy(app)
db = SQLAlchemy()
# 解决sqlite作为后端 => “ValueError: Constraint must have a name"的问题
# db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
