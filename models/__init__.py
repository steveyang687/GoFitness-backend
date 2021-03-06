from .base import db
import pymysql

pymysql.install_as_MySQLdb()


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:33060/gofitness'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    # 下面这句,可有可无(如果使用命令行工具来管理db，下面这一句就可以不要)
    db.create_all(app=app)


