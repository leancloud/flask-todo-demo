# coding: utf-8

import os

from flask import Flask
from flask import redirect
from flask import url_for
from flask import g
from flask import request
from flask import send_from_directory
from flask import flash
from flask import Markup
from flask import render_template
from werkzeug import Request
import leancloud

from views.todos import todos_view
from views.users import users_view


app = Flask(__name__)
app.config.update(dict(PREFERRED_URL_SCHEME='https'))
try:
    app.secret_key = bytes(os.environ.get('SECRET_KEY'), 'utf-8')
except TypeError:
    import sys
    sys.exit('未检测到密钥。请在 LeanCloud 控制台 > 云引擎 > 设置中新增一个名为 SECRET_KEY 的环境变量，再重试部署。')


class HTTPMethodOverrideMiddleware(object):
    """
    使用中间件以接受标准 HTTP 方法
    详见：https://gist.github.com/nervouna/47cf9b694842134c41f59d72bd18bd6c
    """

    allowed_methods = frozenset(['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    bodyless_methods = frozenset(['GET', 'HEAD', 'DELETE', 'OPTIONS'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        method = request.args.get('METHOD', '').upper()
        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = 0
        return self.app(environ, start_response)

# 注册中间件
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
app.wsgi_app = leancloud.HttpsRedirectMiddleware(app.wsgi_app)
app.wsgi_app = leancloud.engine.CookieSessionMiddleware(app.wsgi_app, app.secret_key)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')
app.register_blueprint(users_view, url_prefix='/users')


@app.before_request
def before_request():
    g.user = leancloud.User.get_current()


@app.route('/')
def index():
    return redirect(url_for('todos.show'))


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/robots.txt')
@app.route('/favicon.svg')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
