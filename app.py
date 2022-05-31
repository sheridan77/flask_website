import hashlib
import json
from functools import wraps
import pymysql
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import CSRFProtect
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
csrf = CSRFProtect(app)


def md5(text):
    _md5 = hashlib.md5()
    _md5.update(text.encode('utf-8'))
    return _md5.hexdigest()


def login_valid(fun):
    @wraps(fun)
    def inner(*args, **kwargs):
        username = request.cookies.get('username')
        user_id = request.cookies.get('user_id')
        if username and user_id:
            sql = 'select username from user_info where id = %s'
            cursor.execute(sql, (user_id,))
            res = cursor.fetchone()
            if res:
                if res[0] == username:
                    return fun(*args, **kwargs)
        return redirect('/login/')
    return inner


@app.route('/')
def index():
    return redirect(url_for('login', website_name='facebook'))
    # return redirect(url_for('index_website', website_name='facebook'))


@app.route('/register/', methods=["POST", "GET"])
def register():
    info = ''
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()
        # print(username, password)
        sql = 'select username from user_info where username = %s'
        try:
            cursor.execute(sql, (username,))
            res = cursor.fetchone()
        except pymysql.err.InterfaceError:
            res = 'error'
            info = '用户名不符合规范'
            return render_template('register.html', **locals())
        if not res:
            sql = 'insert into user_info(username, password, keyword_list) values (%s, %s, %s)'
            cursor.execute(sql, (username, md5(password), json.dumps([], ensure_ascii=False)))
            db.commit()
            response = redirect('/login/')
            return response
        elif res == 'error':
            info = '用户名不合法'
            return render_template('register.html', **locals())
        else:
            info = '用户名已存在'
            return render_template('register.html', **locals())
    return render_template('register.html', **locals())


@app.route('/login/', methods=['GET', 'POST'])
def login():
    info = ''
    password_info = ''
    if request.method == 'POST':
        try:
            username = request.form.get('username').strip().lower()
            password = request.form.get('password').strip()
        except AttributeError:
            return render_template('login.html')
        sql = 'select id, username, password from user_info where username = %s'
        try:
            cursor.execute(sql, (username,))
            res = cursor.fetchone()
        except pymysql.err.InterfaceError:
            info = '用户名不合法'
            return render_template('login.html', **locals())
        if res:
            u_id, u_name, ps_word = res
            if md5(password) == ps_word:
                response = redirect('/index/facebook/')
                response.set_cookie('username', username)
                response.set_cookie('user_id', str(u_id))
                return response
            else:
                password_info = '密码错误'
                return render_template('login.html', **locals())
        else:
            info = '用户名不存在'
            return render_template('login.html', **locals())
    return render_template('login.html')


@app.route('/index/<string:website_name>/')
@login_valid
def index_website(website_name):
    return render_template(f'index_{website_name}.html')


@app.route('/facebook/first_page/', methods=['GET', 'POST'])
@login_valid
def facebook_first_page():
    if request.method == 'GET':
        sql = 'select story_fbid, publish_time, content, image ' \
              'from facebook_article ' \
              'where key_word = %s ' \
              'order by publish_time desc'
        cursor.execute(sql, ('mustang', ))
        result = cursor.fetchall()
        res_list = list()
        for res in result:
            story_fbid, publish_time, content, image = res
            if image:
                image = json.loads(image)
            res_list.append(
                {
                    'story_fbid': story_fbid,
                    'publish_time': publish_time,
                    'content': content,
                    'image': image
                }
            )

        return render_template('facebook_index.html', key='Mustang', article=res_list)


# @app.route('/facebook/yours/')
# def facebook_yours():



if __name__ == '__main__':
    db = pymysql.connect(
        host='129.146.45.58',
        user='root',
        password='001224',
        port=3306,
        database='facebook_info',
        use_unicode=True
    )
    # db = pymysql.connect(
    #     host='127.0.0.1',
    #     user='root',
    #     password='001224',
    #     port=3306,
    #     database='facebook_info',
    #     use_unicode=True
    # )
    cursor = db.cursor()
    app.run('0.0.0.0', 7897, debug=True)





