import os

from controllers.index import extra_router  # 导入蓝图实例
from flask import send_from_directory, session, request, render_template, redirect, url_for, abort, jsonify

from app.get_sql_data_nav import get_sql_data_nav, get_sql_posts, get_sql_comments, views_add, get_sql_comments_user, \
    get_sql_comments_num, username_by_id, ins_comment, del_comment, sel_uid_by_uname, sel_secid_by_secname, \
    insert_posts, sel_posts, sel_user_res, del_user_res, del_user_posts, sel_user_courses, del_user_courses

# 确保上传目录存在
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 定位到项目根目录
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')

# 路由函数：用户上传文件
@extra_router.route('/account' , methods=['GET', 'POST'])
def index_up_self():
    if 'user' in session:
        username = session['user']
    else:
        return jsonify("用户没有登录!")
    nav_data = get_sql_data_nav()
    # print(username)
    user_id = username_by_id(username)
    # print(user_id)
    data_posts = sel_posts(user_id)
    data_courses=sel_user_courses(user_id)
    # print(data_courses)
    # # print(data_posts)
#查出选择的课程
#查找出自己发的帖子
    data_res=sel_user_res(user_id)
    print(data_res)
    return render_template('/user/up_posts.html',
                           username=username,
                           data_posts=data_posts,
                           data_res=data_res,
                           data_courses=data_courses,
                           **nav_data)


# 确保上传目录存在
UPLOAD_FOLDER = 'uploads/up_posts_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
IMAGE_FOLDER = os.path.join(UPLOAD_FOLDER, 'images_static')
VIDEO_FOLDER = os.path.join(UPLOAD_FOLDER, 'video')


@extra_router.route('/up_posts', methods=['post'])
def up_posts():

    username = session['user']
    user_id=sel_uid_by_uname(username)['user_id']
    post_title = request.form.get('postTitle')
    post_content = request.form.get('postContent')
    tag = request.form.get('tag')
    comm_tag=request.form.get('section')

    # print(section_id)
    # print(tag)
    # print(section_name)

    if not post_title or not post_content:
        return "缺少标题或内容", 400

    # 获取上传的文件（如果存在）
    files = request.files.getlist('fileUpload[]')
    uploaded_files = []

    for file in files:
        if file.filename:

            extension = os.path.splitext(file.filename)[1]  # 获取文件扩展名

            # 判断文件类型
            if extension in ['.jpg', '.jpeg', '.png', '.gif']:  # 图片扩展名
                save_path = os.path.join(IMAGE_FOLDER, file.filename)
                relative_path = f"/uploads/up_posts_files/images_static/{file.filename}"
            elif extension in ['.mp4', '.avi', '.mov', '.mkv']:  # 视频扩展名
                save_path = os.path.join(VIDEO_FOLDER, file.filename)
                relative_path = f"/uploads/up_posts_files/video/{file.filename}"

        else:
            relative_path =None

        file.save(save_path)
        uploaded_files.append(relative_path)
    insert_posts(comm_tag,tag,user_id,post_title, post_content, relative_path )
    # print(uploaded_files)
    # print(post_title)
    # print(post_content)
    # print(file_path)
    return index_up_self()
#删除资源
@extra_router.route('/del_res/<int:res_id>', methods=['get'])
def del_res(res_id):
    print(res_id)
    del_user_res(res_id)
    return index_up_self()
#删除帖子
@extra_router.route('/del_posts/<int:post_id>',methods=['get'])
def del_posts(post_id):
    del_user_posts(post_id)
    return index_up_self()
#删除课程
@extra_router.route('/del_courses/<int:id>',methods=['get'])
def del_courses(id):
    del_user_courses(id)
    return index_up_self()