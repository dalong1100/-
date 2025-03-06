# run.py
from flask import send_from_directory

from __init__ import create_app

app = create_app()  # 调用工厂函数创建应用实例


@app.route('/uploads/<path:filename>')
def serve_file(filename):

    return send_from_directory('files', filename)
if __name__ == '__main__':
    app.run(debug=True)