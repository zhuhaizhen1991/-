from info.home import home_blu
#使用蓝图对象注册路由
@home_blu.route('/')
def index():
    return 'index'