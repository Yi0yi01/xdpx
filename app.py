from flask import *
import opSql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'px1314'


@app.route('/')
def index():
    print(session)
    if session.get('username') is None:
        return render_template('index.html', newurl='/login', name='', option="登录/注册")
    else:
        if session['priority'] == 0:
            return render_template('index.html', newurl='/logout', name=session.get('username'), option="退出")
        else:
            return render_template('index.html', newurl='/logout', name=session.get('username'), option="管理")


@app.route('/news/')
def news():
    if session.get('username') is None:
        return render_template('news.html', newurl='/login', name='', option="登录/注册")
    else:
        return render_template('news.html', newurl='/logout', name=session.get('username'), option="退出")


@app.route('/athlete')
def athlete():
    if session.get('username') is None:
        return render_template('athlete.html', newurl='/login', name='', option="登录/注册")
    else:
        return render_template('athlete.html', newurl='/logout', name=session.get('username'), option="退出")


@app.route('/about')
def about():
    if session.get('username') is None:
        return render_template('about.html', newurl='/login', name='', option="登录/注册")
    else:
        print(session.get('username'))
        return render_template('about.html', newurl='/logout', name=session.get('username'), option="退出")


@app.route('/matches')
def matches():
    if session.get('username') is None:
        return render_template('matches.html', newurl='/login', name='', option="登录/注册")
    else:
        return render_template('matches.html', newurl='/logout', name=session.get('username'), option="退出")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # print(opSql.login(request.form['name'], request.form['pwd']))
        name = request.form['name']
        pwd = request.form['pwd']
        """
        if name in online:
            print("logined")
            return redirect(url_for('index'))
        
        """

        (f, id) = opSql.login(name, pwd)
        # print(f)
        # session['user_id'] = id
        if f == -1:
            print("error")
            return redirect('login')
        else:
            session['username'] = name
            if f == 0:
                session['id'] = id
                session['priority'] = 0
                return redirect(url_for('index'))
            elif f == 1:
                session['id'] = id
                session['priority'] = 1
                return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """
    session.pop('username')
    session.pop('priority')
    """
    if session.get('username') in online:
        del online[session.get('username')]
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        print(request.form)
        return redirect(url_for('index'))


@app.route('/news/<newsid>')
def getnews(newsid):
    result = opSql.get_news(newsid)
    return render_template('newscontent.html', title=result[0][1], content1=result[0][1], content2=result[0][2])


if __name__ == '__main__':
    app.run()
