from importlib.resources import contents
from random import random

from flask import render_template, session, jsonify,request
from controllers.index import extra_router  # 导入蓝图实例

from app.get_sql_data_nav import sel_courses, get_sql_data_nav, check_if_logged_in, username_by_id, ins_reviews, \
    courses_outline, sel_sections, sel_views, ins_notes, sel_notes, sel_notes01, select_courses, courses_detail
import random


@extra_router.route('/courses', methods=['get'])
def courses_index():
    if 'user' in session:
        username = session['user']
    else:
        username = None

    data_courses=sel_courses()
    print(data_courses)
    nav_data = get_sql_data_nav()
    # print(data_courses[0]['course_id'])
    return render_template("/user/courses.html",
                            data_courses=data_courses,
                            username=username,
                             **nav_data)


#课程详情
@extra_router.route('/courses_details/<int:course_id>', methods=['get'])
def courses_details(course_id):
   # course从0 开始
   #  print(course_id)
   #获取概述、大纲、教师、评论、查
    data_teacher=courses_outline(course_id)
    # print(data_teacher)
   #大纲、章节
    data_sections=sel_sections(course_id)
    # print(data_sections)
   #评论
    data_reviews=sel_views(course_id)
    # print(data_reviews)
    #随机获取相关课程、课程右边
    random_courses = random.sample(sel_courses(),4)
    # print(random_courses)

    if 'user' in session:
        username = session['user']
    else:
        username = None
    nav_data = get_sql_data_nav()


    return render_template('/user/course_details.html',
                           course_id=course_id,
                           data_teacher=data_teacher,
                           data_sections=data_sections,
                           data_reviews=data_reviews,
                           len_reviews=len(data_reviews),
                           username=username,
                           **nav_data,
                           random_courses=random_courses
                           )
#对课程评价
@extra_router.route('/insert_reviews/<int:course_id>',methods=['post'])
def insert_reviews(course_id):
    #检查用户登录
    if not check_if_logged_in():
        return jsonify({"success": False, "message": "用户未登录，无法提交评论"})
    else:
        user_name=session['user']

    # 读取前端内容
    comments=request.form.get('message')
    user_id=username_by_id(user_name)
    ins_reviews(course_id,user_id,comments)
    print(course_id)
    print(comments)
    print(user_id)
    #删除评论
    return jsonify({"success": True, "message": "评论提交成功"})
#选择课程

@extra_router.route('/ins_sec/<int:course_id>/0', methods=['GET'])
def ins_sec(course_id):
    if not check_if_logged_in():
        return jsonify({"status": 401, "message": "用户未登录，无法选择"}), 401
    else:
        print(course_id+1)
        user_name=session['user']
        user_id=username_by_id(user_name)
        print(user_id)
        select_courses(user_id, course_id+1)
        return jsonify({"status": 200, "message": "选择成功"}), 200

#课程播放
@extra_router.route('/cla_dis/<int:course_id>/<int:sections_id>', methods=['get'])
def cla_dis(course_id,sections_id):
    if 'user' in session:
        username = session['user']
    else:
        return "用户没登陆"

    print(course_id)
    # print(userid)
    # print(sections_id)
    data_course=courses_detail(course_id)
    print(data_course)
    nav_data = get_sql_data_nav()
    data_sections01=sel_sections(course_id+1)
    print(data_sections01)
    data_sections=sel_sections(course_id+1)[sections_id-1]
    # print(data_sections)
    #获取笔记内容
    data_note=sel_notes(course_id+1)
    print(data_note)




    return render_template('/user/course_display.html',
                           data_course=data_course,
                           **nav_data,
                           data_note=data_note,
                           course_id=course_id,
                           sections_id=sections_id,
                           data_sections=data_sections,
                           data_sections01=data_sections01,
                           username=username
                           )

#记笔记
@extra_router.route('/insert_notes/<int:course_id>/<int:sections_id>', methods=['POST'])
def insert_notes(course_id, sections_id):
    #获取用户名、id
    if 'user' in session:
        username = session['user']
    else:
        return "用户没登陆"
    userid = username_by_id(username)


    print(userid)
    # 获取前端笔记内容
    content = request.form.get('message')

    print(course_id)
    print(sections_id)
    print(content)

    #查看数据库中是否已经存在笔记
    data_note = sel_notes01(course_id + 1,sections_id)
    print(type(data_note))
    if data_note==():
        ins_notes(userid, course_id+1, sections_id, content)
    else:
        return "已经存在笔记了"

    # 插入数据库

    return cla_dis(course_id,sections_id)














