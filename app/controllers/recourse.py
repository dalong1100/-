import os

from controllers.index import extra_router  # 导入蓝图实例
from flask import send_from_directory, session, request, render_template, redirect, url_for, abort, jsonify

from app.get_sql_data_nav import get_sql_data_nav, get_sql_posts, get_sql_comments, views_add, get_sql_comments_user, \
    get_sql_comments_num, username_by_id, ins_comment, del_comment, sel_uid_by_uname, sel_secid_by_secname, \
    insert_posts, sel_posts, sel_res, sel_high_res, sel_type_resource, sea_res


@extra_router.route('/res', methods=['GET'])
def index_res():
    if 'user' in session:
        username = session['user']
    else:
        username = None
    nav_data = get_sql_data_nav()
    #获取资源
    data_res=sel_res()
    # print(type(data_res))
    # print(data_res)
    data_high_res=sel_high_res()
    # print(type(data_high_res))
    # print(data_high_res)
    return render_template("/user/recourse.html",
                           **nav_data, username=username,
                           data_res=data_res,
                           data_high_res=data_high_res
                           )

#获取不同类型的资源
@extra_router.route('/res/<resource_type>', methods=['GET'])
def sel_type_res(resource_type):
    nav_data = get_sql_data_nav()
    # print(resource_type)
    data_res = sel_type_resource(resource_type)
    # print(type(data_res))
    # print(data_res)
    data_high_res = sel_high_res()
    return render_template("/user/resource.html",
                           **nav_data,
                           data_res=data_res,
                           data_high_res=data_high_res
                           )
#搜索
@extra_router.route('/res_search', methods=['get'])
def sel_type_search_res():
    query = request.args.get('query')
    # print(query)
    nav_data = get_sql_data_nav()
    # print(nav_data)
    data_res = sea_res(query)
    # print(data_res)
    data_high_res = sel_high_res()
    return render_template("/user/resource.html",
                           **nav_data,
                           data_res=data_res,
                           data_high_res=data_high_res
                           )




