from flask import  Flask,request,render_template,session,redirect,url_for,escape, jsonify
from CoTec.utility.date.date_go import DateGo
from datetime import timedelta

import sys
import os

from Spezia2.scan.framework.html_scraper import ExtraHtml

app = Flask(__name__)
app.secret_key = 'xxx'


@app.route('/')
def index():
    return render_template('scan_test.html')

    # if 'username' in session:
    #     # return 'Logged in as %s' % escape(session['username'])
    #     return render_template('scan_test.html')
    # else:
    #     return redirect(url_for('login'))
    #     # return "No User >>> Project Global Hawk  " + DateGo.get_current_date()


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/log')
def log():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')

    return "Log Test"

@app.route('/pid')
def pid():
    return 'PID: ' + str(os.getpid())


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # password = request.args.get('password', '')

        if username != 'global':
            error = 'Invalid username'
        elif password != 'hawk':
            error = 'Invalid password'
        else:
            session['logged_in'] = True

            session['username'] = username
            return redirect(url_for('index'))
        return render_template('manager/login.html', error=error)
    return render_template('manager/login.html',error=error)


# @app.route('/scanTestPage')
# def scanTestPage():
#     return render_template('scan_test.html')


@app.route('/scanTest', methods=['GET', 'POST'])
def scanTest():
    content_url = request.form['content_url']
    content_ruler = request.form['content_ruler']

    content_url = 'http://ent.news.cn/2017-03/16/c_1120637704.htm'
    content_ruler = 'title**:title;date:span class=h-time;content**:div id=p-detail;author**:span class=tiyi1'

    encode = ExtraHtml.get_page_encode(content_url)
    content = ExtraHtml.web_extra_content(content_url, content_ruler, encode)

    # content = jsonify(content)

    res = []
    res = [content_url, content_ruler]

    res = '{ "name": "John" }'

    return jsonify(content)

    # return jsonify(month=[x[0] for x in res],
    #                evaporation=[x[1] for x in res],
    #                precipitation=[x[2] for x in res])
    # error = None
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #
    #     if username != 'global':
    #         error = 'Invalid username'
    #     elif password != 'hawk':
    #         error = 'Invalid password'
    #     else:
    #         session['logged_in'] = True
    #
    #         session['username'] = username
    #         return redirect(url_for('index'))
    #     return render_template('manager/login.html', error=error)
    # return render_template('manager/login.html',error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username',None)
    return redirect(url_for('index'))


@app.route('/exit')
def exit():
    # os.exit(0)
    return "Bye"
    # raise SystemExit
    # return "Bye"


@app.route('/set/<name>')
def show_user_profile(name):
    # show the user profile for that user
    return 'Say %s' % name


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



app.debug = True

app.run(port=3721)

session.permanent = True
app.permanent_session_lifetime = timedelta(minutes=5)
# app.run(host='0.0.0.0')