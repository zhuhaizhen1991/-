from info.modules.home import home_blu
from flask import current_app, render_template, session

from info.utils.models import User


#使用蓝图对象注册路由
@home_blu.route('/')
def index():
    #判断用户是否已经登录
    user_id = session.get('user_id')
    user = None
    if user_id: # 已登录
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 查询点击量前10的新闻
    # rank_list = []
    # try:
    #     rank_list = News.query.order_by(News.clicks)
    #
    # user = user.to_dict() if user else None
    # #将登录数据,排行数据,传入模板渲染
    return render_template('index.html', user=user)


#设置网站图标(浏览器会自动向网站发起/favicon.ico请求,后端只需要实现该路由,并返回图片即可)
@home_blu.route('/favicon.ico')
def favico():
    # flask中封装了语法send_static_file
    #可以获取静态文件的内容,封装为响应对象,并根据内容设置content-type
    response = current_app.send_static_file('news/favicon.ico') #相对路径基于static文件夹而来
    return response