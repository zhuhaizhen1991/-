from flask import g, redirect, url_for, render_template, abort, request, jsonify, current_app

from info.modules.user import user_blu
from info.utils.common import user_login_data, file_upload

#个人中心
from info.utils.response_code import RET, error_map


@user_blu.route('/user_info')
@user_login_data
def user_info():
    user = g.user
    if not user:  # 用户未登录,重定向到前台首页
        return  redirect(url_for('home.index'))

    return render_template('user.html',user = user.to_dict())


#基本资料
@user_blu.route('/base_info',methods = ["GET","POST"])
@user_login_data
def base_info():
    user = g.user
    if not user:# 未登录
        return abort(403)

    if request.method == 'GET':# GET 展示页面
        return render_template('user_base_info.html',user=user.to_dict())

    #POST 提交资料

    #获取参数
    signature = request.json.get('signature')
    nick_name = request.json.get('nick_name')
    gender = request.json.get('gender')
    #校验参数
    if not all([signature,nick_name,gender]):
        return jsonify(errno = RET.PARAMERR,errmsg = error_map[RET.PARAMERR])

    if gender not in['MAN',"WOMAN"]:
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    #修改用户数据
    user.nick_name = nick_name
    user.signature = signature
    user.gender = gender

    #json返回
    return jsonify(errno = RET.OK,errmsg = error_map[RET.OK])


#头像设置
@user_blu.route('/pic_info',methods = ['GET','POST'])
@user_login_data
def pic_info():
    user = g.user
    if not user:
        return abort(403)

    if request.method == 'GET': # GET展示页面
        return render_template('user_pic_info.html',user = user.to_dict())

    #post提交资料

    #获取参数
    avatar_file = request.files.get('avatar')

    #获取文件数据
    try:
        file_bytes = avatar_file.read()
        # print(file_bytes)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.PARAMERR,errmsg = error_map[RET.PARAMERR])
        
    #上传文件到七牛云服务器 一般会将文件单独管理起来 业务服务器 文件服务器
    try:
        file_name = file_upload(file_bytes)
    except Exception as e:
        current_app.lgger.error(e)
        return jsonify(errno = RET.THIRDERR,errmsg = error_map[RET.THIRDERR])
    #修改头像链接
    user.avatar_url = file_name

    #json返回 必须返回头像链接
    return  jsonify(errno = RET.OK,errmsg = error_map[RET.OK],data=user.to_dict())










