from datetime import timedelta
from flask import Flask, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from config import ProductionConfig
from info import create_app

app = create_app('dev')

#创建管理器
mgr = Manager(app)
#使用管理器生成迁移命令
mgr.add_command('mc',MigrateCommand)

@app.route('/index')
def index():
    session['name'] = 'zhangsan'
    return '首页'

if __name__ == '__main__':
    mgr.run()