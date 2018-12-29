from flask import current_app, render_template

from info.home import home_blu


#使用蓝图对象注册路由
@home_blu.route('/')
def index():

    return render_template('index.html')

#设置网站图标(浏览器会自动向网站发起/favicon.ico请求,后端只需要实现该路由,并返回图片即可)
@home_blu.route('/favicon.ico')
def favico():
    # flask中封装了语法send_static_file
    #可以获取静态文件的内容,封装为响应对象,并根据内容设置content-type
    response = current_app.send_static_file('news/favicon.ico') #相对路径基于static文件夹而来
    return response