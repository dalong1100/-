import random

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, Response, send_file
import os

from app.get_sql_data_nav import sel_adm_login, sel_num_user, sel_num_courses, sel_num_resources, sel_num_posts, \
    sel_high_stu, sel_res, sel_high_res, select_posts, sel_courses, sea_courses, del_course, up_course, \
    sel_tea, sel_cour_talk, sea_talk, del_view, sel_sec, del_coure_sec, update_sec, sel_course_id_by_course_name, \
    add_sections, searc_sec, sel_res_high, update_res, del_user_res, sea_res, sel_resource_type, sel_file_type, \
    username_by_id, insert_res, adm_sel_posts, get_sql_data_nav, update_posts_comm_tag, del_user_posts, \
    adm_search_posts, adm_select_comments, adm_select_all_comments, adm_select_users, adm_update_users, adm_user_study, \
    user_id_by_username, adm_user_posts, adm_user_comments, adm_user_res, adm_user_class, admin_user_class, \
    admin_user_study, admin_user_comments, admin_user_posts, admin_user_res

admin_bp = Blueprint('admin', __name__,template_folder='templates')
#模板返回
@admin_bp.route('/admin')
def admin_page():
    if 'admin' in session:
        return redirect(url_for('admin.admin_index'))
    else:
        return render_template("/admin/adm_login.html")
#处理登录逻辑
@admin_bp.route('/adm_login', methods=['GET', 'POST'])
def adm_login():
    email = request.form.get('email')
    password = request.form.get('password')

    # 调试：检查接收到的 email 和 password
    print(f"接收到的 email: {email}, 密码: {password}")

    data = sel_adm_login()  # 假设你按照 email 查询数据库

    if data:
        sql_email = data[0]['email']
        sql_password = data[0]['password']
        print(f"数据库中的 email: {sql_email}, 密码: {sql_password}")  # 调试输出

        if sql_email == email and sql_password == password:
            # 登录成功
            username = data[0]['username']
            session['admin'] = username  # 将用户名存入 session
            return jsonify({
                "status": "success",
                "message": "登录成功",
                "redirect": "/adm_index"
            })
        else:
            # 密码不匹配
            return jsonify({
                "status": "error",
                "message": "密码或者用户名不正确",
                "redirect": None
            })
    else:
        # 用户未找到
        return jsonify({
            "status": "error",
            "message": "出现错误、联系管理员处理",
            "redirect": None
        })

#管理员登录之后模板
@admin_bp.route('/adm_index')
def admin_index():
    if 'admin' in session:
        username = session['admin']
    else:
        return jsonify("用户未登录")
    data_login=sel_adm_login()[0]



    #学员数量
    num_user=sel_num_user()['count(*)']
    #课程数量
    num_courses = sel_num_courses()['count(*)']
    #资源数量
    num_resources = sel_num_resources()['count(*)']
    high_resources = sel_high_res()
    # print(high_resources)
    #帖子数量
    num_posts = sel_num_posts()['count(*)']
    high_posts=select_posts()
    # print(high_posts)
    # print(num_user, num_courses, num_resources, num_posts)

    #学员数据（学生姓名、学习课程、学习时间、平均学习量、资源下载量、学习日期）、难点：学习时间、资源下载量
    data=sel_high_stu()


    # print(data)
    return render_template("/admin/adm_index.html",
                           username=username,
                           data_login=data_login,
                           num_user=num_user,
                           num_courses=num_courses,
                           num_resources=num_resources,
                           num_posts=num_posts,
                           data=data,
                           high_resources=high_resources,
                           high_posts=high_posts)
#管理员退出登录
@admin_bp.route('/adm_logout')
def adm_logout():
    if 'admin' in session:
        session.pop('admin', None)
        return redirect(url_for('admin.admin_page'))
    else:
        return "用户未登录"



#课程信息
@admin_bp.route('/adm_courses')
def adm_courses():

    #学员数量
    num_user=sel_num_user()['count(*)']
    #课程数量
    num_courses = sel_num_courses()['count(*)']
    #资源数量
    num_resources = sel_num_resources()['count(*)']
    #所有课程信息
    sel_all_courses=sel_courses()
    # 所有教师信息
    sel_all_tea = sel_tea()
    print(sel_all_tea)
    print(sel_all_courses)

    return render_template('admin/course/adm_courses.html',
                           num_user=num_user,
                           num_courses=num_courses,
                           num_resources=num_resources,
                           sel_all_courses=sel_all_courses,
                           sel_all_tea=sel_all_tea

                           )
#课程搜索
@admin_bp.route('/sear_source', methods=['GET', 'POST'])
def sear_source():
    sear_source=request.form.get('search')
    # print(sear_source)

    # 学员数量
    num_user = sel_num_user()['count(*)']
    # 课程数量
    num_courses = sel_num_courses()['count(*)']
    # 资源数量
    num_resources = sel_num_resources()['count(*)']
    # 所有课程信息
    sel_all_courses=sea_courses(sear_source)

    print(sel_all_courses)
    return render_template('admin/course/adm_courses.html',
                    num_user=num_user,
                    num_courses=num_courses,
                    num_resources=num_resources,
                    sel_all_courses=sel_all_courses

                  )
#课程操作--删除
@admin_bp.route('/del_cour/<int:course_id>', methods=['get'])
def del_cour(course_id):
    del_course(course_id)
    return '删除成功'
# 课程查看
@admin_bp.route('/sel_cour/<int:course_id>', methods=['get'])
def del_sel(course_id):

    return redirect(url_for('extra_router.courses_details',course_id=course_id))

#课程更新
@admin_bp.route('/update_course/<int:course_id>', methods=['post'])
def update_course(course_id):
    #获取数据
    course_name = request.form.get('course_name')
    course_desc = request.form.get('course_desc')
    teacher_id = request.form.get('teacher_id')
    course_cat = request.form.get('course_cat')
    course_type = request.form.get('course_type')
    print(course_id,course_name, course_desc,teacher_id, course_cat, course_type)
    # 更新数据(数据方便、需要根据teacher_name找出teacher_id)
    up_course(teacher_id,course_name,course_desc,course_cat ,course_type, course_id)

    return redirect(url_for('admin.adm_courses'))
#课程评论--主页
@admin_bp.route('/courses_talk_index/', methods=['get'])
def courses_talk_index():
    if 'admin' in session:
        username = session['admin']
    else:
        return jsonify("用户未登录")
    # 学员数量
    num_user = sel_num_user()['count(*)']
    # 课程数量
    num_courses = sel_num_courses()['count(*)']
    # 资源数量
    num_resources = sel_num_resources()['count(*)']
    #课程评论
    sel_all_courses = sel_courses()

    sel_talk=sel_cour_talk()
    print(sel_talk)
    # sel_cour_talk(course_id)
    return render_template("/admin/course/adm_courses_talk.html",
                           sel_all_courses=sel_all_courses,
                           sel_talk=sel_talk,
                           sel_user=username,
                           username=username,
                           num_user=num_user,
                           num_courses=num_courses,
                           num_resources=num_resources,
                           )
@admin_bp.route('/sear_talk', methods=['GET', 'POST'])
#课程评论--搜索
def sear_talk():
    if 'admin' in session:
        username = session['admin']
    else:
        return jsonify("用户未登录")
    data_login=sel_adm_login()[0]

    sear_source=request.form.get('search')
    print(sear_source)

    # 学员数量
    num_user = sel_num_user()['count(*)']
    # 课程数量
    num_courses = sel_num_courses()['count(*)']
    # 资源数量
    num_resources = sel_num_resources()['count(*)']
    # 所有课程信息
    sel_all_courses=sea_talk(sear_source)
    sel_talk=sel_cour_talk()
    print(sel_talk)

    return render_template('admin/course/adm_courses_talk.html',
                    username=username,
                    data_login=data_login,
                    num_user=num_user,
                    num_courses=num_courses,
                    num_resources=num_resources,
                    sel_talk=sel_talk,
                    sel_all_courses=sel_all_courses

                  )
#课程评论--删除
@admin_bp.route('/del_talk/<int:review_id>',  methods=['GET', 'POST'])
def del_talk(review_id):
    #删除评论
    del_view(review_id)
    print(review_id)
    return redirect(url_for('admin.courses_talk_index'))
#课程章节--查看
#查看服务器中已经存在的课程章节视频

FILE_DIRECTORY = "uploads/up_posts_files/video"





@admin_bp.route('/adm_sear_sec/', methods=['GET', 'POST'])
def sear_sec():
    if 'admin' in session:
        username = session['admin']
    else:
        return jsonify("用户未登录")
    data_login=sel_adm_login()[0]
      #学员数量
    num_user=sel_num_user()['count(*)']
    #课程数量
    num_courses = sel_num_courses()['count(*)']
    #资源数量
    num_resources = sel_num_resources()['count(*)']
    #课程章节--查看
    sec_data=sel_sec()
    print(sec_data)
    #将课程对应的章节存入一个嵌套列表中

    nested_dict = {}

    # 遍历列表中的每个章节
    for section in sec_data:
        course_name = section['course_name']
        # course_id = section['course_id']
        # 如果课程名称不在嵌套字典中，则添加它并创建一个空列表来存储章节
        course_key = (section['course_id'], section['course_name'])
        if course_key not in nested_dict:
            nested_dict[course_key] = {
                'course_id': section['course_id'],
                'course_name': section['course_name'],
                'sections': []
            }
        # 从章节字典中移除不需要的键（例如course_id和可能的course_name，因为它们在嵌套结构中已经隐含了）
        # 这里我们假设只保留与章节直接相关的键
        nested_dict[course_key]['sections'].append( {
            'section_ID': section['section_ID'],
            'section_name': section['section_name'],
            'section_num': section['section_num'],
            'section_URL': section['section_URL'],
            'section_des': section['section_des'],
            'section_date': section['section_date']
        })

        # 将处理后的章节字典添加到对应课程的列表中
        # nested_dict[course_name].append(section_for_dict)
        # nested_dict[course_id].append(section_for_dict)
        # transformed_data = [value for key, value in nested_dict.items()]
    # 打印嵌套字典以验证结果
    transformed_data = [value for key, value in nested_dict.items()]

    # 输出转换后的数据以验证结果
    for course in transformed_data:
        print(course)





    files = os.listdir(FILE_DIRECTORY)







    post=None







    return render_template("/admin/course/adm_courses_sections.html",
                    files=files,
                    post=post,
                   sec_data=sec_data,
                   username=username,
                   data_login=data_login,
                   num_user=num_user,
                   num_courses=num_courses,
                   num_resources=num_resources,
                   courses=transformed_data,
                           )
#删除章节--section_id
@admin_bp.route('/del_cour_sec/<int:sections_id>', methods=['GET', 'POST'])
def del_cour_sec(sections_id):
    print(sections_id)
    del_coure_sec(sections_id)
    return redirect(url_for('admin.sear_sec'))
#更新章节--
@admin_bp.route('/update_cour_sec/<int:sections_id>', methods=['post'])
def update_cour_sec(sections_id):
    sec_name = request.form.get('sec_name')
    sec_desc = request.form.get('sec_desc')
    sec_file_name = request.form.get('sec_file_name')
    sec_file_url='/'+FILE_DIRECTORY+'/'+sec_file_name
    print(sec_name,sec_desc,sec_file_name,sec_file_url,sections_id)
    update_sec(sec_name, sec_desc, sec_file_url, sections_id)
    return redirect(url_for('admin.sear_sec'))
#增加章节-------------------------------------------------------------缺少文件上传 --目前只是将文件名存取、并未存文件到服务器--------------
@admin_bp.route('/add_sec', methods=[ 'POST'])
def add_sec():
    course_name = request.form.get('course_name')

    course_id=sel_course_id_by_course_name(course_name)['course_id']
    sec_name = request.form.get('sec_name')
    print(sec_name)
    sec_res=request.form.get('sec_res')
    sec_desc=request.form.get('sec_desc')
    section_URL='/'+FILE_DIRECTORY+'/'+sec_res
    add_sections(course_id, sec_name, section_URL, sec_desc)
    print(course_id)
    print(course_name, sec_name,sec_res, sec_desc,section_URL)
    return redirect(url_for('admin.sear_sec'))

#搜索章节
@admin_bp.route('/sea_sec', methods=['GET', 'POST'])
def sea_sec():

    if 'admin' in session:
        username = session['admin']
    else:
        return jsonify("用户未登录")
    data_login = sel_adm_login()[0]
    # 学员数量
    num_user = sel_num_user()['count(*)']
    # 课程数量
    num_courses = sel_num_courses()['count(*)']
    # 资源数量
    num_resources = sel_num_resources()['count(*)']
    # 课程章节--查看
    value=request.form.get('value')
    sec_data = searc_sec(value)
    print(sec_data)
    # 将课程对应的章节存入一个嵌套列表中

    nested_dict = {}

    # 遍历列表中的每个章节
    for section in sec_data:
        course_name = section['course_name']
        # course_id = section['course_id']
        # 如果课程名称不在嵌套字典中，则添加它并创建一个空列表来存储章节
        if course_name not in nested_dict:
            nested_dict[course_name] = []
            # nested_dict[course_id] = []

        # 从章节字典中移除不需要的键（例如course_id和可能的course_name，因为它们在嵌套结构中已经隐含了）
        # 这里我们假设只保留与章节直接相关的键
        section_for_dict = {
            'section_ID': section['section_ID'],
            'section_name': section['section_name'],
            'section_num': section['section_num'],
            'section_URL': section['section_URL'],
            'section_des': section['section_des'],
            'section_date': section['section_date']
        }

        # 将处理后的章节字典添加到对应课程的列表中
        nested_dict[course_name].append(section_for_dict)
        # nested_dict[course_id].append(section_for_dict)

    # 打印嵌套字典以验证结果
    print(nested_dict)

    files = os.listdir(FILE_DIRECTORY)

    post = None

    return render_template("/admin/course/adm_courses_sections.html",
                           files=files,
                           post=post,
                           sec_data=sec_data,
                           username=username,
                           data_login=data_login,
                           num_user=num_user,
                           num_courses=num_courses,
                           num_resources=num_resources,
                           courses=nested_dict,
                           )
#资源信息
#初始化

@admin_bp.route('/res_index', methods=['GET', 'POST'])
def res_index():
    #获取下载量前五的资源名称和下载量
    #字典转换成列表
    labels = []
    values = []

    for row in range(7):
        labels.append(sel_res_high()[row]['name'])
        values.append(sel_res_high()[row]['download_count'])
        # print(labels,values)
    if 'admin' not in session:
        return jsonify("用户未登录")
    # 将数据传递到前端
    else:
        username = session['admin']
    data_login = sel_adm_login()[0]
    # 学员数量
    num_user = sel_num_user()['count(*)']
    # 课程数量
    num_courses = sel_num_courses()['count(*)']
    # 资源数量
    num_resources = sel_num_resources()['count(*)']
    # 课程章节--查看
    res_data = sel_res_high()
    # print(res_data)
    return render_template('admin/resource/adm_res_index.html',
                           labels=labels,
                           values=values,
                           res_data=res_data,
                           username=username,
                           data_login=data_login,
                           num_user=num_user,
                           num_courses=num_courses,
                           num_resources=num_resources,
                           )
# 资源信息-- 更新----------------------------------------------------缺少上传文件到服务器的代码、 缺少选择上传的用户功能 ---------------------
@admin_bp.route('/update_res/<int:res_id>/<string:file_type>/<int:user_id>', methods=['GET', 'POST'])
def update_reso(res_id,file_type,user_id):
    # print(res_id)
    res_name = request.form.get('res_name')
    res_desc = request.form.get('res_desc')
    url = request.form.get('res_url')
    folder='/uploads/study_resource/'
    res_url=folder+url
    res_type = request.form.get('res_type')
    print(res_id,res_name,file_type,user_id,res_type,res_url,res_desc)
    if 'admin' in session:
        update_res(res_id,res_name,file_type,user_id,res_type,res_url,res_desc)
    else:
        return jsonify("用户未登录")
    return redirect(url_for('admin.res_index'))
#删除资源
@admin_bp.route('/adm_del_res/<int:res_id>', methods=['GET', 'POST'])
def adm_del_res(res_id):
    print(res_id)
    #删除资源
    if 'admin' in session:
        del_user_res(res_id)
        return redirect(url_for('admin.res_index'))
    return redirect(url_for('admin.res_index'))
#搜索显示
@admin_bp.route('/adm_sel_res', methods=['GET', 'POST'])
def adm_sel_res():
    if 'admin' in session:
        query=request.form.get('search')
        # print(query)
        # 获取下载量前五的资源名称和下载量
        # 字典转换成列表
        labels = []
        values = []

        for row in range(7):
            labels.append(sel_res_high()[row]['name'])
            values.append(sel_res_high()[row]['download_count'])
            # print(labels, values)
        if 'admin' not in session:
            return jsonify("用户未登录")
        # 将数据传递到前端
        else:
            username = session['admin']
        data_login = sel_adm_login()[0]
        # 学员数量
        num_user = sel_num_user()['count(*)']
        # 课程数量
        num_courses = sel_num_courses()['count(*)']
        # 资源数量
        num_resources = sel_num_resources()['count(*)']
        # 课程章节--查看
        res_data = sea_res(query)
        print(res_data)
        return render_template('admin/resource/adm_res_index.html',
                               labels=labels,
                               values=values,
                               res_data=res_data,
                               username=username,
                               data_login=data_login,
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               )
    return redirect(url_for('admin.res_index'))
#上传资源
@admin_bp.route('/adm_up_res', methods=['GET', 'POST'])
def adm_up_res():
    if 'admin' in session:
        username = session['admin']
        num_user = sel_num_user()['count(*)']
        # 课程数量
        num_courses = sel_num_courses()['count(*)']
        # 资源数量
        num_resources = sel_num_resources()['count(*)']
        sel_all_resource_type=sel_resource_type()
        # print(sel_all_resource_type)
        sel_all_file_type=sel_file_type()
        # print(sel_all_file_type)


        return render_template("/admin/resource/adm_up_res.html",
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               username=username,
                               sel_all_file_type=sel_all_file_type,
                               sel_all_resource_type=sel_all_resource_type
                               )
    else:
        return render_template("/admin/adm_login.html")
#获取表单数据插入数据库

@admin_bp.route('/up_res', methods=['POST'])
def up_res():
    if 'admin' in session:
        username = session['admin']
        res_name = request.form.get('res_name')
        res_desc = request.form.get('res_desc')
        resource_type = request.form.get('resource_type')
        files = request.files.get('res_file')
        print(files.filename)
        # print(type(files))
        # res_file = request.form.get('res_file')
        # folder = '/uploads/study_resource/'
        # resource_path=folder+res_file
        user_name = request.form.get('user_name')
        user_id=username_by_id(user_name)
# 存储文件
        # 确保上传目录存在
        UPLOAD_FOLDER = 'uploads/study_resource'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# 获取上传的文件（如果存在）
        uploaded_files = []
        file_type = (os.path.splitext(files.filename)[1])[1:]  # 获取文件扩展名
        print(file_type)

        if files.filename:
            now = datetime.now()
            time = now.strftime("%Y_%m_%d_%H_%M")
            file=files.filename
            files_path= username+'_'+time+'_'+file
            print(files)
            print(files.filename)
            print(files_path)
            # files.filename= username
            extension = os.path.splitext(files.filename)[1]  # 获取文件扩展名
            # 判断文件类型
            if extension in ['.jpg', '.jpeg', '.png', '.gif']:  # 图片扩展名
                save_path = os.path.join( UPLOAD_FOLDER, files_path)
                relative_path = f"/uploads/study_resource/{files_path}"
            elif extension in ['.mp4', '.avi', '.mov', '.mkv']:  # 视频扩展名
                save_path = os.path.join( UPLOAD_FOLDER, files.files_path)
                relative_path = f"/uploads/study_resource/{files_path}"
        else:
            relative_path = None
        files.save(save_path)
        uploaded_files.append(relative_path)
        insert_res(res_name, file_type, user_id, resource_type, relative_path, res_desc)
        print(res_name, file_type, user_id, resource_type, relative_path, res_desc)
        return redirect(url_for('admin.res_index'))
#帖子信息
@admin_bp.route('/post_index', methods=['GET', 'POST'])
def post_index():
    if 'admin' in session:
        #柱状图
        # 获取下载量前五的资源名称和下载量
        # 字典转换成列表
        labels = []
        values = []

        for row in range(7):
            labels.append(adm_sel_posts()[row]['title'])
            values.append(adm_sel_posts()[row]['views'])
            print(labels, values)

        username = session['admin']
        num_user = sel_num_user()['count(*)']
        num_courses = sel_num_courses()['count(*)']
        num_resources = sel_num_resources()['count(*)']
        post_data = adm_sel_posts()
        print(post_data)
        nav_data = get_sql_data_nav()
        return render_template('/admin/posts/adm_posts.html',
                               username=username,
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               post_data=post_data,
                               labels=labels,
                               values=values,
                               **nav_data
                               )
    else:
        return jsonify("管理员未登录")
#更新帖子内容-- 只能更新帖子的所属板块
@admin_bp.route('/adm_update_post/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if 'admin' in session:
        print(post_id)

        post_comm_tag=request.form.get('post_comm_tag')
        # update_posts_comm_tag(post_id,  post_comm_tag)
        print(post_comm_tag)
        return redirect(url_for('admin.post_index'))
    else:
        return redirect(url_for('admin.admin_index'))
#删除帖子
@admin_bp.route('/adm_delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if 'admin' in session:
        del_user_posts(post_id)
        return redirect(url_for('admin.post_index'))
    else:
        return redirect(url_for('admin.admin_index'))
#搜索资源信息
@admin_bp.route('/adm_sea_posts', methods=['GET', 'POST'])
def adm_sea_posts():
    if 'admin' in session:
        # 柱状图
        # 获取下载量前五的资源名称和下载量
        # 字典转换成列表
        query = request.form.get('query')
        labels = []
        values = []

        for row in range(7):
            labels.append(adm_sel_posts()[row]['title'])
            values.append(adm_sel_posts()[row]['views'])
            print(labels, values)

        username = session['admin']
        num_user = sel_num_user()['count(*)']
        num_courses = sel_num_courses()['count(*)']
        num_resources = sel_num_resources()['count(*)']
        post_data = adm_search_posts(query)
        print(post_data)
        nav_data = get_sql_data_nav()
        return render_template('/admin/posts/adm_posts.html',
                               username=username,
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               post_data=post_data,
                               labels=labels,
                               values=values,
                               **nav_data
                               )
    else:
        return redirect(url_for('admin.admin_index'))
#帖子的评论信息
#处理的是comments表信息
#初始化
@admin_bp.route('/adm_comments_index', methods=['GET', 'POST'])
def adm_comments_index():
    if 'admin' in session:
        # 柱状图
        # 获取下载量前五的资源名称和下载量
        # 字典转换成列表
        query = request.form.get('query')
        labels = []
        values = []

        for row in range(7):
            labels.append(adm_select_comments()[row]['title'])
            values.append(adm_select_comments()[row]['comment_count'])

        # print(labels, values)
        username = session['admin']
        num_user = sel_num_user()['count(*)']
        num_courses = sel_num_courses()['count(*)']
        num_resources = sel_num_resources()['count(*)']
        #根据query获取数据
        post_data =adm_select_comments()
        print(post_data)
        nav_data = get_sql_data_nav()
        return render_template('/admin/posts/adm_post_comments_index.html',
                               username=username,
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               post_data=post_data,
                               labels=labels,
                               values=values,
                               **nav_data
                               )
    else:
        return redirect(url_for('admin.admin_index'))
#----------------------搜索帖子--------------------------------------
@admin_bp.route('/adm_comments_search', methods=['GET', 'POST'])
def adm_comments_search():
    if 'admin' in session:
        # 柱状图
        # 获取下载量前五的资源名称和下载量
        # 字典转换成列表
        query = request.form.get('query')
        labels = []
        values = []

        for row in range(7):
            labels.append(adm_select_comments()[row]['title'])
            values.append(adm_select_comments()[row]['comment_count'])

        # print(labels, values)
        username = session['admin']
        num_user = sel_num_user()['count(*)']
        num_courses = sel_num_courses()['count(*)']
        num_resources = sel_num_resources()['count(*)']

        post_data = null
        print(post_data)
        nav_data = get_sql_data_nav()
        return render_template('/admin/posts/adm_post_comments_index.html',
                               username=username,
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               post_data=post_data,
                               labels=labels,
                               values=values,
                               **nav_data
                               )
    else:
        return redirect(url_for('admin.admin_index'))


#------------------------帖子评论的增删改未完成---------------------------












#学员基本信息
@admin_bp.route('/adm_search_users', methods=['GET', 'POST'])
def adm_search_users():
    if 'admin' in session:
        # 柱状图
        # 获取下载量前五的资源名称和下载量
        # 字典转换成列表


        # print(labels, values)
        username = session['admin']
        num_user = sel_num_user()['count(*)']
        num_courses = sel_num_courses()['count(*)']
        num_resources = sel_num_resources()['count(*)']

        user_data = adm_select_users()

        print(type(user_data))
        nav_data = get_sql_data_nav()
        return render_template('/admin/user/user_info.html',
                               username=username,
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               user_data=user_data,
                               **nav_data
                               )
    else:
        return redirect(url_for('admin.admin_index'))
#更新学员基本信息
@admin_bp.route('/update_user_info', methods=['GET', 'POST'])
def update_user_info():
    if 'admin' in session:
        username=request.form.get('username')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        email = request.form.get('email')
        url = request.form.get('user_url')
        user_url='/uploads/user_info/user/'+str(url)
        type=request.form.get('type')
        # print(username, user_id, password, email, user_url, type)
        #更新数据
        adm_update_users(username, password, email, user_url, type, user_id)
        return redirect(url_for('admin.adm_search_users'))
    else:
        return "error"
#学员学习基本信息
@admin_bp.route('/user_sel_class', methods=['GET', 'POST'])
def user_sel_class():
    if 'admin' in session:
        # 柱状图
        # 获取下载量前五的资源名称和下载量
        # 字典转换成列表


        # print(labels, values)
        username = session['admin']
        num_user = sel_num_user()['count(*)']
        num_courses = sel_num_courses()['count(*)']
        num_resources = sel_num_resources()['count(*)']

        user_data = adm_user_study()
        print(user_data)
        nav_data = get_sql_data_nav()
        return render_template('/admin/user/user_sel_class.html',
                               username=username,
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               user_data=user_data,
                               **nav_data
                               )
    else:
        return redirect(url_for('admin.admin_index'))
@admin_bp.route('/user_study_info/<int:user_id>', methods=['GET', 'POST'])
def user_study_info(user_id):
    if 'admin' in session:
        username = session['admin']
        num_user = sel_num_user()['count(*)']
        num_courses = sel_num_courses()['count(*)']
        num_resources = sel_num_resources()['count(*)']
        uname=user_id_by_username(user_id)
        #发布帖子
        data_post=adm_user_posts(user_id)
        print(data_post)

        #评论帖子
        data_comments =adm_user_comments(user_id)
        print(data_comments)
        #发布资源
        data_res =adm_user_res(user_id)
        print(data_res)
        #选择课程信息
        data_class =adm_user_class(user_id)
        print(data_class)

        nav_data = get_sql_data_nav()
        return render_template('/admin/user/user_sel_info.html',
                               username=username,
                               num_user=num_user,
                               num_courses=num_courses,
                               num_resources=num_resources,
                               uname=uname,
                               data_post=data_post,
                               data_comments=data_comments,
                               data_res=data_res,
                               data_class=data_class,
                               **nav_data
                               )

    else:
        return redirect(url_for('admin.admin_index'))


# 导出学生信息
import pandas as pd
from datetime import datetime, time


@admin_bp.route('/output_user_info', methods=['GET', 'POST'])
def output_user_info():
    if 'admin' in session:
        username = session['admin']
        output_class=admin_user_class()
        output_study=admin_user_study()
        output_comments=admin_user_comments()
        output_res=admin_user_res()
        output_posts=admin_user_posts()
        print(output_class,output_study,output_comments,output_res)
        columns_class=output_class[0].keys()
        columns_study=output_study[0].keys()
        columns_comments=output_comments[0].keys()
        columns_res=output_res[0].keys()
        columns_posts=output_posts[0].keys()
        df1 = pd.DataFrame(output_class, columns=columns_class)
        df2 = pd.DataFrame(output_study, columns=columns_study)
        df3 = pd.DataFrame(output_comments, columns=columns_comments)
        df4 = pd.DataFrame(output_res, columns=columns_res)
        df5 = pd.DataFrame(output_posts, columns=columns_posts)
        now = datetime.now()
        time = now.strftime("%Y_%m_%d_%H_%M_%S")
        # 导出为 Excel 文件
        output_dir = 'uploads/download'  # 相对路径（当前目录下的 output 文件夹）
        file = username+'_'+time+'.xlsx'  # 输出文件名
        output_file = os.path.join(output_dir, file)
        with pd.ExcelWriter(output_file) as writer:
            df1.to_excel(writer, sheet_name='选课表', index=True)
            df2.to_excel(writer, sheet_name='学习情况表', index=True)
            df3.to_excel(writer, sheet_name='课程评论表', index=True)
            df4.to_excel(writer, sheet_name='上传资源表', index=True)
            df5.to_excel(writer, sheet_name='发布帖子表', index=True)
        return send_file(output_file, as_attachment=True)
    else:
        return "用户未登录"






