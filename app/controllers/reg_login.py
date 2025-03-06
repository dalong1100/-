from controllers.index import extra_router  # 导入蓝图实例
from flask import render_template, request, session, redirect, url_for

from app.get_sql_data_nav import check_if_logged_in, get_sql_data_nav, ins_logtime, username_by_id, ins_logoutime
from app.mysql import con_my_sql


#------------------------------------------------登陆注册------------------------------------------------------------
#网页跳转返回模板文件--登录界面和注册界面、返回导航栏查询到的数据
@extra_router.route('/login' ,methods=['get'])
def acc_login():
    if check_if_logged_in():
        return "用户已经登录"
    else:
        nav_data = get_sql_data_nav()
        return render_template("/user/acc_login.html", **nav_data)


@extra_router.route('/register' , methods=['get'])
def acc_reg():
    nav_data = get_sql_data_nav()

    return render_template("/user/acc_reg.html", **nav_data)




@extra_router.route('/acc_login' ,methods=['post'])
def login():
    email = request.form.get('email')
    pwd = request.form.get('password')
    code = "select * from user where email='%s'" % (email)
    cursor_ans = con_my_sql(code)
    cursor_select = cursor_ans.fetchall()
    # print(cursor_select)
    # print(type(cursor_select))
    # # print(username)
    if  cursor_select:
        username=cursor_select[0]['username']
        if pwd == cursor_select[0]['password']:
            session['user'] = username  # 登录成功，将用户名存入 session
            #登陆时间插入数据库
            user_id=username_by_id(username)
            ins_logtime(user_id)
            return redirect(url_for('extra_router.index'))
        else:
            return "密码错误"
    else:
        return "用户不存在"

@extra_router.route('/acc_reg' , methods=['post'])
def reg():
    name = request.form.get('username')
    pwd = request.form.get('password')
    email = request.form.get('email')
    # print(f"Username: {name}, Password: {pwd}, Email: {email}")
    #注册成功后，自动登录并将用户名存入session
    session['user'] = name  # 存储用户登录信息

    code = "select * from user where email='%s'" % (email)
    cursor_ans = con_my_sql(code)
    # print(cursor_ans)
    cursor_select = cursor_ans.fetchall()
    if len(cursor_select) > 0:
        return "邮箱已经注册"
    else:
        code = "INSERT INTO user (username, password,email,user_url) VALUES ('%s', '%s','%s','%s')" % (name, pwd, email, '/uploads/user_info/user/example01.png')
        con_my_sql(code)
    return "注册成功"
@extra_router.route('/logout')
def logout():
    username=session['user']
    user_id = username_by_id(username)
    ins_logoutime(user_id)
    session.pop('user', None)  # 清除 session 中的用户信息
    return redirect(url_for('extra_router.index'))  # 跳转到首页

