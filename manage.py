from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db

# 核心对象为什么要拆分
app = create_app()
# 创建管理对象
manager = Manager(app)

# 创建db管理工具 =》app,db
# 由于此处，使用的是sqlite数据库，sqlite数据库不支持删除操作
# migrate = Migrate(app,db)
# manager.add_command('db',MigrateCommand)
with app.app_context():
    migrate = Migrate()
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

# 注册一个命令
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777)
