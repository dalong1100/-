# __init__.py
from flask import Flask

from app.controllers.admin import admin_bp


def create_app():
    app = Flask(__name__,  template_folder='templates',static_folder='static')
    # 导入蓝图
    from controllers.index import extra_router  # 蓝图定义在 index.py 中
    import controllers.courses  # 确保课程路由被加载到蓝图中
    import controllers.comm
    import controllers.reg_login
    import controllers.posts
    import controllers.recourse
    import controllers.admin
    # 注册蓝图
    app.register_blueprint(extra_router)
    app.register_blueprint(admin_bp)
    app.secret_key = 'your_secret_key'  # 用于加密 session 数据
    return app
