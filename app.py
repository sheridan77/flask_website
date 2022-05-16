import json
import pymysql
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('index_website', website_name='facebook'))


@app.route('/index/<string:website_name>/')
def index_website(website_name):
    return render_template(f'index_{website_name}.html')


@app.route('/facebook/first_page')
def facebook_first_page():
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


if __name__ == '__main__':
    # db = pymysql.connect(
    #     host='44.201.112.75',
    #     user='root',
    #     password='001224',
    #     port=3306,
    #     database='facebook_info',
    #     use_unicode=True
    # )
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='001224',
        port=3306,
        database='facebook_info',
        use_unicode=True
    )
    cursor = db.cursor()
    app.run('0.0.0.0', 5050, debug=True)





