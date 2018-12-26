from datetime import timedelta
from flask import Flask, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

app = Flask(__name__)

# 定义配置类来封装配置信息
class Config:
    DEBUG = True  #设置调试模式
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/info22'#数据库连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False #是否追踪数据库变化
    REDIS_HOST = '127.0.0.1' #redis的连接地址 将自定义的配置也封装到config类中
    REDIS_PORT = 6379
    SESSION_TYPE = 'redis'#设置session存储的方式,redis性能好,方便设置过期时间
    SESSION_REDIS = Redis(host=REDIS_HOST,port=REDIS_PORT)#设置redis链接对象,组件会使用该对象将session数据保存到redis中
    SESSION_USE_SIGNER = True #设置sessionid进行加密
    SECRET_KEY = 'test'#设置sessionid秘钥
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

#从对象中加载配置
app.config.from_object(Config)

#创建mysql连接对象
db = SQLAlchemy(app)
#创建redis连接对象
rs = Redis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

#初始化session存储对象
Session(app)

#创建管理器
mgr = Manager(app)
#初始化迁移器
Migrate(app,db)
#使用管理器生成迁移命令
mgr.add_command('mc',MigrateCommand)


@app.route('/index')
def index():
    session['name'] = 'lisi'
    return '首页'

if __name__ == '__main__':
    mgr.run()