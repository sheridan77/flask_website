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
    return render_template('facebook_index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', 5050, debug=True)





