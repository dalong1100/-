import os

from controllers.index import extra_router  # 导入蓝图实例
from flask import send_from_directory, session, request, render_template, redirect, url_for, abort

from app.get_sql_data_nav import get_sql_data_nav, get_sql_posts, get_sql_comments, views_add, get_sql_comments_user, \
    get_sql_comments_num, username_by_id, ins_comment, del_comment, sel_uid_by_uname, sel_secid_by_secname, \
    insert_posts, select_posts

# 确保上传目录存在
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 定位到项目根目录
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
#------------------------------------------------交流社区（帖子详情） ------------------------------------------------------------

#解析用户发帖的文件路径路由
@extra_router.route('/uploads/<path:filename>')
def serve_uploads(filename):
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_from_directory(UPLOADS_DIR, filename)


@extra_router.route('/comm', methods=['GET'])
def comm():

    if 'user' in session:
        username = session['user']
    else:
        username = None

    # 获取 `section_id` 参数，默认为 None，类型为 int
    comm_tag = request.args.get('comm_tag')
    # print(comm_tag)
    # 调用导航数据函数
    nav_data = get_sql_data_nav()

    # 根据 `section_id` 获取对应的文章数据
    nav_data01 = get_sql_posts(comm_tag)
    # print(nav_data01)
    posts = nav_data01['nav_data_comm_ports']
    # print(posts)
    # 获取分页参数，默认显示第一页
    page = request.args.get('page', default=1, type=int)
    per_page = 3  # 每页显示的文章数量

    # 计算分页相关数据
    total_posts = len(posts)  # 总文章数量
    total_pages = (total_posts + per_page - 1) // per_page  # 计算总页数
    start = (page - 1) * per_page
    end = start + per_page
    page_posts = posts[start:end]  # 当前页的文章切片
    # 渲染模板
    print(page_posts)
    return render_template(
        "/user/comm.html",
        **nav_data,  # 包含导航栏的必要数据
        posts=page_posts,  # 当前页显示的文章
        current_page=page,  # 当前页码
        comm_tag=comm_tag,  # 当前筛选的板块 ID
        total_pages=total_pages ,# 总页数
        username=username,
    )

#-----------------------------------------------------------帖子详情、发表评论------------------------------------------------------------------------------------
# 在Flask应用中定义的路由
@extra_router.route('/comm_details/<int:post_id>',methods=['get'])
def comm_details(post_id):
    if 'user' in session:
        username = session['user']
    else:
        username = None
    nav_data = get_sql_data_nav()
# --------------------------------------------------------帖子详情------------------------------------------------------------------------
    # 根据post_id获取post表文章 浏览次数、简介、时间、详情、类别（？？？？）
    res01=get_sql_comments(post_id)
    # print(res01)
    if not res01:
        return "帖子未找到", 404
    post_detail01 = res01[0]
    #浏览量+1
    views_add(post_id)
    # print(post_id)
    res02 = get_sql_comments_user(post_id)
    count = get_sql_comments_num(post_id) # 确保返回的是整数类型
    comment02= res02
    print(comment02)
#侧边栏随机获取
    data_side=select_posts()
    # print(data_side)

    return render_template('/user/comm_details.html',
                           **nav_data,
                           post=post_detail01,
                           comments=comment02,
                           count_query=count['COUNT(*)'],
                           post_id=post_id,
                           username=username,
                           data_side=data_side
                        )

# --------------------------------------------------------评论管理----------------------------------------------------------------------------------
@extra_router.route('/insert_comments/<int:post_id>',methods=['post'])
def insert_comments(post_id):
    # 读取前端内容
    comments=request.form.get('message')
    user_name=session['user']
    user_id=username_by_id(user_name)
    #前端内容插入数据库
    ins_comment(user_id,post_id,comments)
    #删除评论
    return  comm_details(post_id)

#删除评论
@extra_router.route('/del_comments/<int:comment_id>/<int:post_id>', methods=['get'])
def del_comments(comment_id,post_id):
    # 删除评论
    del_comment(comment_id)
    return redirect(url_for('extra_router.comm_details',post_id=post_id))










