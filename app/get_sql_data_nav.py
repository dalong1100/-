

from flask import session

from mysql import con_my_sql

# 获取导航栏数据 nav
def get_sql_data_nav():



    # 学习
    code_c = "select * from courses order by rand() limit 4"
    nav_select_c = con_my_sql(code_c).fetchall()


    # # 资源中心
    # code_resource = "select * from resource"
    # nav_select_resource = con_my_sql(code_resource).fetchall()


    # 资源中心-学习资料
    code_resource_study = "SELECT DISTINCT SUBSTRING_INDEX(filetype, ':', -1) AS type_without_prefix FROM download_files WHERE filetype LIKE '学习资料:%';"
    nav_resource_study = con_my_sql(code_resource_study).fetchall()

    # 资源中心-试题测试
    code_resource_extest = "SELECT DISTINCT SUBSTRING_INDEX(filetype, ':', -1) AS type_without_prefix FROM download_files WHERE filetype LIKE '试题测试:%';"
    nav_resource_extest = con_my_sql(code_resource_extest).fetchall()

    # 资源中心-拓展资源
    code_resource_extend = "SELECT DISTINCT SUBSTRING_INDEX(filetype, ':', -1) AS type_without_prefix FROM download_files WHERE filetype LIKE '拓展资源:%';"
    nav_resource_extend = con_my_sql(code_resource_extend).fetchall()

    # 交流社区
    code_comm = "SELECT DISTINCT tag FROM posts"
    nav_select_posts= con_my_sql(code_comm).fetchall()
    # 帖子tag内容
    code_posts = "select DISTINCT comm_tag from posts"
    nav_select_comm  = con_my_sql(code_posts).fetchall()
    # print(nav_select_posts)



    return {
        'nav_select_c': nav_select_c,
        # 'nav_select_resource': nav_select_resource,
        'nav_resource_study': nav_resource_study,
        'nav_resource_extest': nav_resource_extest,
        'nav_resource_extend': nav_resource_extend,
        'nav_select_comm': nav_select_comm,
        'nav_select_posts': nav_select_posts
    }
#-------------------------------------------------------交流社区--------------------------------------------------------------------
#获取帖子数据 posts表
def get_sql_posts(comm_tag):
    code_comm_ports = "SELECT posts.*, user.username,user.type FROM posts JOIN user ON posts.user_id = user.user_id  where comm_tag='%s' ORDER BY created_at DESC" % (comm_tag)
    data_comm_ports = con_my_sql(code_comm_ports).fetchall()
    return {  'nav_data_comm_ports': data_comm_ports}
#获取评论数据    comments表
def get_sql_comments(post_id):
    # 根据post_id获取post表文章 浏览次数、简介、时间、详情、类别（？？？？）

    code_ports_details ="SELECT posts.*, user.username FROM posts JOIN user ON posts.user_id = user.user_id WHERE posts.post_id = '%s'"% (post_id)
    data_comm_ports_details = con_my_sql(code_ports_details).fetchall()
    return data_comm_ports_details

def get_sql_comments_user(post_id):
    code_comments_user="SELECT comments.*, user.username,user.user_url FROM comments JOIN user ON comments.user_id = user.user_id WHERE comments.post_id = '%s'"% (post_id)
    data_comments_user=con_my_sql(code_comments_user).fetchall()
    # print(data_comments_user)
    return data_comments_user
def get_sql_comments_num(post_id):
    code_sql_comments_num= "SELECT COUNT(*) FROM comments WHERE post_id = '%s'" % (post_id)
    data_comments_num=con_my_sql(code_sql_comments_num).fetchone()
    return data_comments_num
#发表帖子
def insert_posts(comm_tag,tag,user_id,post_title,post_content,file_path):
    code_insert_posts="insert into posts (comm_tag,tag,user_id,title,content,image_url) values('%s','%s','%s','%s','%s','%s') " %(comm_tag,tag,user_id,post_title,post_content,file_path)
    con_my_sql(code_insert_posts)
    return 0
#随机获取文章
def select_posts():
    code="select p.*,u.username,u.user_url from posts p join user u on p.user_id=u.user_id order by rand() limit 4"
    data=con_my_sql(code).fetchall()
    return data


def sel_uid_by_uname(username):
    code="select user_id from user where username='%s'" %(username)
    user_id=con_my_sql(code).fetchone()
    return user_id
#通过section_name 查 section_id
def sel_secid_by_secname(section_name):
    code="select section_id from community_sections where section_name='%s'" %(section_name)
    section_id=con_my_sql(code).fetchone()
    return section_id
#浏览量+1
#通过课程名称查课程id
def sel_course_id_by_course_name(course_name):
    code="select course_id from courses where course_name='%s'" %(course_name)
    course_id=con_my_sql(code).fetchone()
    return course_id
def views_add(post_id):
    code = "UPDATE posts SET views = views + 1 WHERE post_id = '%s'" %(post_id)
    con_my_sql(code)
    return 0
#通过username查user_id
def username_by_id(username):
    code="select user_id from user where username = '%s'" %(username)
    username=con_my_sql(code).fetchone()['user_id']
    # print(username)
    return username
#通过user_id查username
def user_id_by_username(user_id):
    code="select username from user where user_id = '%s'" %(user_id)
    result=con_my_sql(code).fetchone()['username']
    # print(username)
    return result
#插入评论
def ins_comment(user_id,post_id,content):
    code="insert into comments(user_id,post_id,content) values ('%s','%s','%s')" %(user_id,post_id,content)
    con_my_sql(code)
    return 0
#删除评论
def del_comment(comment_id):
    code="delete from comments where comment_id = '%s'" %(comment_id)
    con_my_sql(code)
    return 0
#----------------------------------------------------------------课程------------------------------------------------------------
def sel_courses():
    code="SELECT c.*,t.*,COUNT(s.section_id) AS section_count,(SELECT COUNT(*) FROM reviews r WHERE r.course_id = c.course_id) AS review_count FROM courses c JOIN teachers t ON c.teacher_id = t.teacher_id LEFT JOIN sections s ON c.course_id = s.course_id GROUP BY c.course_id, c.course_name, c.course_url, c.course_type, t.teacher_name, t.teacher_url ORDER BY c.course_id;"
    data_courses=con_my_sql(code).fetchall()
    return data_courses
def courses_detail(course_id):
    code="SELECT c.*,t.*,COUNT(s.section_id) AS section_count,(SELECT COUNT(*) FROM reviews r WHERE r.course_id = c.course_id) AS review_count FROM courses c JOIN teachers t ON c.teacher_id = t.teacher_id LEFT JOIN sections s ON c.course_id = s.course_id where s.course_id='%s' GROUP BY c.course_id, c.course_name, c.course_url, c.course_type, t.teacher_name, t.teacher_url  ORDER BY c.course_id" %(course_id)
    data_courses=con_my_sql(code).fetchone()
    return data_courses
def courses_outline(course_id):
    code="SELECT c.*,t.* FROM courses c JOIN teachers t  ON c.teacher_id = t.teacher_id WHERE c.course_id= '%s'" %(course_id)
    data_courses=con_my_sql(code).fetchone()
    return data_courses
#选择自己的课程
def select_courses(user_id, course_id):
    code="insert into sel_courses (user_id, course_id) VALUES ('%s', '%s')"%(user_id, course_id)
    con_my_sql(code)
    return 0
def sel_sections(course_id):
    code="select * from sections where course_id ='%s'"%(course_id)
    data=con_my_sql(code).fetchall()
    return data
def sel_views(course_id):
    code="SELECT user.username,user.user_url, reviews.* FROM  user JOIN reviews ON user.user_id = reviews.user_id where course_id ='%s'"%(course_id)
    data = con_my_sql(code).fetchall()
    return data
def ins_reviews(course_id,user_id,review_content):
    code="insert into reviews(course_id,user_id,review_content) values ('%s','%s','%s')" %(course_id,user_id,review_content)
    data=con_my_sql(code)
    return 0
#-------------------------------------------------检查登录---------------------------------------------
def check_if_logged_in():
    if 'user' not in session:
        return False
    return True
# 插入笔记
def ins_notes(user_id,course_id,section_id,content):
    code="insert into notes(user_id,course_id,section_id,content) values ('%s','%s','%s','%s')" %(user_id,course_id,section_id,content)
    con_my_sql(code)
    return 0
#获取笔记内容
def sel_notes(course_id):
    code="select * from notes where course_id='%s'"%(course_id)
    data=con_my_sql(code).fetchall()
    return data
#判断是不是有这个笔记
def sel_notes01(course_id,section_id):
    code = "select * from notes where course_id='%s'and section_id='%s'" % (course_id,section_id)
    data = con_my_sql(code).fetchall()
    return data
#查出自己发的帖子
def sel_posts(user_id):
    code="select * from posts where user_id='%s'" %(user_id)
    data=con_my_sql(code).fetchall()
    return data
# 获取资源
def sel_res():
    code="SELECT resources.*, user.type,user.username FROM resources JOIN user ON resources.user_id = user.user_id"
    data=con_my_sql(code).fetchall()
    return data
#查询热门资源
def sel_high_res():
    code="select * from resources order by download_count desc limit 5"
    data=con_my_sql(code).fetchall()
    return data
#根据资源类型查找
def sel_type_resource(resource_type):
    code="SELECT resources.*, user.type,user.username FROM resources JOIN user ON resources.user_id = user.user_id where resource_type = '%s'" %(resource_type)
    data=con_my_sql(code).fetchall()
    return data
#搜索资源
def sea_res(query):
    code="SELECT resources.*, user.type,user.username FROM resources JOIN user ON resources.user_id = user.user_id  WHERE type LIKE '%s' OR username LIKE '%s' OR resource_type LIKE '%s' OR name LIKE '%s' OR description LIKE '%s'" %('%' + query + '%','%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%')
    data=con_my_sql(code).fetchall()
    return data
#找出自己的帖子-- 个人中心
def sel_user_res(userid):
    code = "SELECT resources.*,user.user_id  FROM resources JOIN user ON resources.user_id = user.user_id where user.user_id = '%s'" % (userid)
    data = con_my_sql(code).fetchall()
    return data
#删除自己的资源
def del_user_res(res_id):
    code="DELETE FROM resources WHERE id = '%s'" %(res_id)
    con_my_sql(code)
    return 0
#删除自己的帖子
def del_user_posts(post_id):
    code="DELETE FROM posts WHERE post_id = '%s'" %(post_id)
    con_my_sql(code)
    return 0
#查找自己的课程
def sel_user_courses(user_id):
    code="select sel_courses.*,courses.* from courses  JOIN sel_courses ON courses.course_id =sel_courses.course_id WHERE user_id='%s'" %(user_id)
    data=con_my_sql(code).fetchall()
    return data
#删除自己的课程
def del_user_courses(id):
    code="DELETE FROM sel_courses WHERE id='%s'" %(id)
    con_my_sql(code)
    return 0
#教学管理登录
def sel_adm_login():
    code="select * from user where type='管理员'"
    result=con_my_sql(code).fetchall()
    return result
#学员数量
def sel_num_user():
    code="select count(*) from user where type='普通学者' or  type='高级学者'"
    result=con_my_sql(code).fetchone()
    return result
#课程数量
def sel_num_courses():
    code="select count(*) from courses"
    result = con_my_sql(code).fetchone()
    return result
#资源数量
def sel_num_resources():
    code="select count(*) from resources"
    result=con_my_sql(code).fetchone()
    return result
#帖子数量
def sel_num_posts():
    code="select count(*) from posts"
    result = con_my_sql(code).fetchone()
    return result
#学生数据
def sel_high_stu():
    code="SELECT user.username, courses.course_name, user_login_sessions.* FROM user_login_sessions JOIN user ON user_login_sessions.user_id = user.user_id JOIN sel_courses ON sel_courses.user_id = user.user_id JOIN courses ON sel_courses.course_id = courses.course_id"
    result = con_my_sql(code).fetchall()
    return result
#将登陆时间存入数据库
def ins_logtime(user_id):
    code="INSERT INTO user_login_sessions (user_id, login_time) VALUES ('%s',NOW())" %(user_id)
    con_my_sql(code)
    # code01="select session_id from user_login_sessions where user_id='%s'" %(user_id)
    # result=con_my_sql(code01).fetchone()
    return 0
#将退出登陆时间存入数据库
def ins_logoutime(user_id):
    code="UPDATE user_login_sessions SET logout_time = NOW() WHERE user_id = '%s' AND logout_time IS NULL" %(user_id)
    con_my_sql(code)
    return 0
#搜索课程
def sea_courses(query):
    code="SELECT c.*,t.* FROM courses c JOIN teachers t ON  c.teacher_id = t.teacher_id  WHERE c.course_name LIKE '%s' OR c.course_desc LIKE '%s' OR t.teacher_name LIKE '%s' OR c.course_cat LIKE '%s' OR c.course_type LIKE '%s'" %('%' + query + '%','%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%')
    data=con_my_sql(code).fetchall()
    return data
def del_course(c_id):
    code="DELETE FROM courses WHERE course_id='%s'" %(c_id)
    con_my_sql(code)
    return 0
#查找出所有的教师
def sel_tea():
    code="select teacher_id,teacher_name from teachers"
    result=con_my_sql(code).fetchall()
    return result
#根据教师名查找id
#更新课程
def up_course(teacher_id,course_name,course_desc,course_cat ,course_type, course_id):
    code="update courses set teacher_id='%s',course_name='%s',course_desc='%s',course_cat='%s' ,course_type='%s' where course_id='%s'" %(teacher_id,course_name,course_desc,course_cat,course_type, course_id)
    con_my_sql(code)
    return 0
#查找所有课程的评论
def sel_cour_talk():
    code="SELECT reviews.*, user.username FROM reviews JOIN user ON reviews.user_id = user.user_id"
    result=con_my_sql(code).fetchall()
    return result
def sea_talk(query):
    code="SELECT c.*,t.*,COUNT(s.section_id) AS section_count,(SELECT COUNT(*) FROM reviews r WHERE r.course_id = c.course_id) AS review_count FROM courses c JOIN teachers t ON c.teacher_id = t.teacher_id LEFT JOIN sections s ON c.course_id = s.course_id WHERE (c.course_name LIKE '%s' OR t.teacher_name LIKE '%s' or s.section_id LIKE '%s') GROUP BY c.course_id, c.course_name, c.course_url, c.course_type, t.teacher_name, t.teacher_url ORDER BY c.course_id;" %('%' + query + '%','%' + query + '%', '%' + query + '%')
    data=con_my_sql(code).fetchall()
    return data
def del_view(review_id):
    code="delete from reviews where review_id='%s'" %(review_id)
    con_my_sql(code)
    return 0
def sel_sec():
    code="SELECT c.course_name,s.* FROM sections s INNER JOIN courses c ON s.course_id = c.course_id"
    result=con_my_sql(code).fetchall()
    print(type(result))
    return result
#删除章节
def del_coure_sec(section_id):
    code="DELETE FROM sections WHERE section_id='%s'" %(section_id)
    code01 = "UPDATE sections JOIN (SELECT section_ID,ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY section_num) AS new_section_num FROM sections) AS ordered_sections ON sections.section_ID = ordered_sections.section_ID SET sections.section_num = ordered_sections.new_section_num;"
    con_my_sql(code01)
    con_my_sql(code)
    return 0
#更新章节
def update_sec(section_name,section_des,section_url,section_id):
    code="UPDATE sections SET section_name = '%s',section_des = '%s',section_url = '%s',section_date=NOW() WHERE section_id = '%s'"%(section_name,section_des,section_url,section_id)
    con_my_sql(code)
    return 0
#增加章节
def add_sections(course_id,section_name,section_URL,section_des):
    code="INSERT INTO sections (course_id, section_name, section_URL, section_des, section_date) VALUES ('%s', '%s','%s', '%s',  NOW());" %(course_id,section_name,section_URL,section_des)
    code01="UPDATE sections JOIN (SELECT section_ID,ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY section_num) AS new_section_num FROM sections) AS ordered_sections ON sections.section_ID = ordered_sections.section_ID SET sections.section_num = ordered_sections.new_section_num;"
    con_my_sql(code)
    con_my_sql(code01)
    return 0
#搜索章节
def searc_sec(value):
    code = "SELECT c.course_name,s.* FROM sections s INNER JOIN courses c ON s.course_id = c.course_id where c.course_name LIKE '%s' or s.section_name LIKE '%s' or s.section_url LIKE '%s' or s.section_des LIKE '%s' "%('%' + value + '%','%' + value + '%','%' + value + '%','%' + value + '%')
    result=con_my_sql(code).fetchall()
    return result
#柱状图
def sel_res_high():
    code="SELECT * FROM resources ORDER BY download_count DESC"
    result=con_my_sql(code).fetchall()
    # print(type(result))
    return result
#更新资源
def update_res(id,name,file_type,user_id,resource_type,resource_path,description):
    code="update resources set name='%s',file_type='%s',user_id='%s',resource_type='%s',resource_path='%s',description='%s',upload_date=NOW() where id='%s'" %(name,file_type,user_id,resource_type,resource_path,description,id)
    con_my_sql(code)
    return 0
#上传资源时、方便选择资源类型、和 文件类型
def sel_resource_type():
    code="SELECT DISTINCT resource_type FROM resources"
    result=con_my_sql(code).fetchall()
    return result
def sel_file_type():
    code="SELECT DISTINCT file_type FROM resources"
    result=con_my_sql(code).fetchall()
    return result
#插入资源
def insert_res(name, file_type, user_id, resource_type, resource_path, description):
    code="INSERT INTO resources (name, file_type, user_id, resource_type, resource_path, description) VALUES ('%s','%s','%s','%s','%s','%s')" %(name, file_type, user_id, resource_type, resource_path, description)
    con_my_sql(code)
    return 0
#获取所有帖子的信息（包含用户名）
def adm_sel_posts():
    code="select p.*,u.username,u.user_url from posts p join user u on p.user_id=u.user_id"
    result=con_my_sql(code).fetchall()
    return result
#更新帖子内容-- 只能更新帖子的所属板块
def update_posts_comm_tag(post_id,comm_tag):
    code="update posts set comm_tag='%s' where post_id='%s'" %(comm_tag,post_id)
    con_my_sql(code)
    return 0
#搜索帖子
def adm_search_posts(query):
    code="select p.*,u.username,u.user_url from posts p join user u on p.user_id=u.user_id where p.title LIKE '%s' or u.username LIKE '%s' or comm_tag LIKE '%s' or views LIKE '%s'" %('%' + query + '%','%' + query + '%','%' + query + '%','%' + query + '%')
    result=con_my_sql(code).fetchall()
    # print(result)
    return result
#帖子评论的大概信息（post_id、title、数量）
def adm_select_comments():
    code="SELECT p.post_id, p.title, COUNT(c.comment_id) AS comment_count FROM posts p LEFT JOIN comments c ON p.post_id = c.post_id GROUP BY p.post_id, p.title"
    result=con_my_sql(code).fetchall()
    return result
# #根据query获取数据
# def adm_sea_select_comments():
#     code="SELECT p.post_id, p.title, COUNT(c.comment_id) AS comment_count FROM posts p LEFT JOIN comments c ON p.post_id = c.post_id GROUP BY p.post_id, p.title"
#     result=con_my_sql(code).fetchall()
#     return result
#comments表的所有数据
def adm_select_all_comments(post_id):
    code="SELECT * FROM comments WHERE post_id='%s' " %(post_id)
    result=con_my_sql(code).fetchall()
    print(result)
    return result
def adm_select_users():
    code="SELECT * FROM user "
    result=con_my_sql(code).fetchall()
    print(result)
    return result
#根据user_id来更新user的信息
def adm_update_users(username,password,email,user_url,type,user_id):
    code="update user set username='%s',password='%s', email='%s', user_url='%s',type='%s' where user_id='%s'" %(username,password,email,user_url,type,user_id)
    con_my_sql(code)
    return 0
#查询用户id、 选课数量、发帖数量、上传资源数量、帖子评论数量
def adm_user_study():
    code="SELECT u.user_id,u.username,COALESCE(c.comment_count, 0) AS comment_count,COALESCE(sc.sel_courses_count, 0) AS sel_courses_count,COALESCE(p.posts_count, 0) AS posts_count,COALESCE(r.resources_count, 0) AS resources_count,COALESCE(rv.reviews_count, 0) AS reviews_count,COALESCE(note.notes_count, 0) AS notes_count FROM user u LEFT JOIN (SELECT user_id, COUNT(*) AS comment_count FROM comments GROUP BY user_id) c ON u.user_id = c.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS sel_courses_count FROM sel_courses GROUP BY user_id) sc ON u.user_id = sc.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS posts_count FROM posts GROUP BY user_id) p ON u.user_id = p.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS resources_count FROM resources GROUP BY user_id) r ON u.user_id = r.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS reviews_count FROM reviews GROUP BY user_id) rv ON u.user_id = rv.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS notes_count FROM notes GROUP BY user_id) note ON u.user_id = note.user_id"
    result=con_my_sql(code).fetchall()
    print(type(result))
    return result
# 发布帖子
def adm_user_posts(user_id):
    code="SELECT posts.*, COUNT(comments.post_id) AS comment_count FROM posts LEFT JOIN comments ON posts.post_id = comments.post_id WHERE posts.user_id ='%s'  GROUP BY posts.post_id" %(user_id)
    result=con_my_sql(code).fetchall()
    return result
# 评论帖子
def adm_user_comments(user_id):
    code="SELECT comments.*, posts.title FROM comments  JOIN posts ON comments.post_id = posts.post_id where comments.user_id='%s'" %(user_id)
    result=con_my_sql(code).fetchall()
    return result
# 发布资源
def adm_user_res(user_id):
    code="SELECT * FROM resources where user_id='%s'" %(user_id)
    result=con_my_sql(code).fetchall()
    return result
# 选择课程信息
def adm_user_class(user_id):
    code="SELECT c.course_name,sc.*,r.*,(SELECT COUNT(*) FROM notes n WHERE n.course_id = sc.course_id) AS note_count FROM sel_courses sc JOIN courses c ON sc.course_id = c.course_id LEFT JOIN reviews r ON sc.course_id = r.course_id AND sc.user_id = r.user_id WHERE sc.user_id = '%s'" %(user_id)
    result=con_my_sql(code).fetchall()
    return result
#所有结果集
def admin_user_class():
    code="SELECT c.course_name,sc.*,r.*,(SELECT COUNT(*) FROM notes n WHERE n.course_id = sc.course_id) AS note_count FROM sel_courses sc JOIN courses c ON sc.course_id = c.course_id LEFT JOIN reviews r ON sc.course_id = r.course_id AND sc.user_id = r.user_id "
    result=con_my_sql(code).fetchall()
    return result
def admin_user_study():
    code="SELECT u.user_id,u.username,COALESCE(c.comment_count, 0) AS comment_count,COALESCE(sc.sel_courses_count, 0) AS sel_courses_count,COALESCE(p.posts_count, 0) AS posts_count,COALESCE(r.resources_count, 0) AS resources_count,COALESCE(rv.reviews_count, 0) AS reviews_count,COALESCE(note.notes_count, 0) AS notes_count FROM user u LEFT JOIN (SELECT user_id, COUNT(*) AS comment_count FROM comments GROUP BY user_id) c ON u.user_id = c.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS sel_courses_count FROM sel_courses GROUP BY user_id) sc ON u.user_id = sc.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS posts_count FROM posts GROUP BY user_id) p ON u.user_id = p.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS resources_count FROM resources GROUP BY user_id) r ON u.user_id = r.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS reviews_count FROM reviews GROUP BY user_id) rv ON u.user_id = rv.user_id LEFT JOIN (SELECT user_id, COUNT(*) AS notes_count FROM notes GROUP BY user_id) note ON u.user_id = note.user_id"
    result=con_my_sql(code).fetchall()
    print(type(result))
    return result
# 发布帖子
def admin_user_posts():
    code="SELECT posts.*, COUNT(comments.post_id) AS comment_count FROM posts LEFT JOIN comments ON posts.post_id = comments.post_id GROUP BY posts.post_id"
    result=con_my_sql(code).fetchall()
    return result
# 评论帖子
def admin_user_comments():
    code="SELECT comments.*, posts.title FROM comments  JOIN posts ON comments.post_id = posts.post_id "
    result=con_my_sql(code).fetchall()
    return result
# 发布资源
def admin_user_res():
    code="SELECT * FROM resources"
    result=con_my_sql(code).fetchall()
    return result



