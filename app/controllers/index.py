# controllers/index.py
import os

from flask import Blueprint, render_template, session

from app.get_sql_data_nav import get_sql_data_nav

# 创建蓝图实例
extra_router = Blueprint('extra_router', __name__)

# 主页路由
@extra_router.route('/', methods=['GET'])
def index():
    if 'user' in session:
        username = session['user']
    else:
        username = None
    nav_data = get_sql_data_nav()
    print(nav_data)

    return render_template("/user/index.html", **nav_data, username=username)
