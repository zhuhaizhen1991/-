import time
from datetime import datetime, timedelta

from flask import request, render_template, current_app, url_for, redirect, session, g

from info.modules.admin import admin_blu
from info.utils.common import user_login_data
from info.utils.models import User


@admin_blu.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET': #GET 展示页面

        #取出session数据
        user_id = session.get('user_id')
        is_admin = session.get('is_admin')
        if user_id and is_admin: #管理员已登录,重定向到后台首页
            return redirect(url_for('admin.index'))

        return render_template('admin/login.html')


    #POST 提交资料
    #获取参数
    username = request.form.get('username')
    password = request.form.get('password')
    #校验参数
    if not all([username,password]):
        return render_template('admin/login.html',errmsg = '参数不足')
    #获取管理员用户数据  is_admin = True
    try:
        user = User.query.filter(User.mobile == username,User.is_admin==True).first()
    except Exception as e:
        current_app.logger.error(e)
        return render_template('admin/login.html',errmsg = '数据库操作失败')

    if not user: # 判断用户是否存在
        return render_template('admin/login.html',errmsg = '管理员不存在')

    #校验密码
    if not user.check_password(password):
        return render_template('admin/login.html',errmsg='账号/密码错误')

    #保存session数据 实现免密码登录
    session['user_id'] = user.id
    session['is_admin'] = True

    #校验成功,重定向到后台首页
    return  redirect(url_for('admin.index'))

#后台退出登录
@admin_blu.route('/')
def logout():
    session.pop('user_id',None)
    session.pop('is_admin',None)
    #重定向到后台登录页面
    return redirect(url_for('admin.login'))


#后台首页
@admin_blu.route('/index')
@user_login_data
def index():
    return render_template('admin/index.html',user = g.user.to_dict())

#用户统计
@admin_blu.route('/user_count')
def user_count():

    #用户总数(除了管理员之外)
    try:
        total_count = User.query.filter(User.is_admin == False).count()
    except Exception as e:
        current_app.logger.error(e)
        total_count = 0


    #月新增人数  注册时间 >= 本月1号0点(默认是从0点开始)
    #获取当前时间的年和月
    t = time.localtime()

    #构建日期字符串  2019-01-01
    mon_date_str = '%d-%02d-01'%(t.tm_year,t.tm_mon)
    #转换为日期对象
    mon_date = datetime.strptime(mon_date_str,"%Y-%m-%d")

    try:
        mon_count = User.query.filter(User.is_admin == False,User.create_time >= mon_date).count()
    except Exception as e:
        current_app.logger.error(e)
        mon_count = 0

    #日新增人数  注册时间>=本月本日0点,<次日0点
    #构建日期字符串  2019-01-05
    day_date_str = "%d-%02d-%02d"%(t.tm_year,t.tm_mon,t.tm_mday)

    #转换为日期对象
    day_date = datetime.strptime(day_date_str,"%Y-%m-%d")

    try:
        day_count = User.query.filter(User.is_admin == False,User.create_time >= day_date).count()
    except Exception as e:
        current_app.logger.error(e)
        day_count = 0

    #某日的注册人数  注册时间 >= 当日0点 ,<次日0点
    active_count = []
    active_time = []

    for i in range(0,30):
        begin_date = day_date - timedelta(days=i) #当日0点
        end_date = begin_date + timedelta(days=1) #次日0点

        try:
            one_day_count = User.query.filter(User.is_admin == False,User.create_time >= begin_date,User.create_time < end_date).count()

            active_count.append(one_day_count) #存放日期对应的注册人数

            #将日期对象转为日期字符串
            one_day_str = begin_date.strftime("%Y-%m-%d")
            active_time.append(one_day_str) #存放日期字符串

        except Exception as e:
            current_app.logger.error(e)
            one_day_count = 0

    #日期和注册量倒序
    active_time.reverse()
    active_count.reverse()

    data = {
        'total_count':total_count,
        'mon_count':mon_count,
        'day_count':day_count,
        'active_count':active_count,
        'active_time':active_time
    }

    return render_template('admin/user_count.html',data = data)















