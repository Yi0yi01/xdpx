from flask import *
import opSql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'px1314'


@app.route('/')
def index():
    # print(session)
    if session.get('username') is None:
        return render_template('index.html', newurl='/login', name='', option="登录/注册")
    else:
        return render_template('index.html', name=session.get('username'), priority=session.get('priority'))


@app.route('/news/')
def news():
    news = opSql.get_all_news()
    # imgs = opSql.get_cover_imgs()
    # print(news)
    # print(imgs)
    if session.get('username') is None:
        return render_template('news.html', newurl='/login', name='', option="登录/注册", resp=news)
    else:
        return render_template('news.html', name=session.get('username'), priority=session.get('priority'), resp=news)


@app.route('/athlete')
def athlete():
    if session.get('username') is None:
        return render_template('athlete.html', newurl='/login', name='', option="登录/注册")
    else:
        return render_template('athlete.html', name=session.get('username'), priority=session.get('priority'))


@app.route('/about')
def about():
    if session.get('username') is None:
        return render_template('about.html', newurl='/login', name='', option="登录/注册")
    else:
        # print(session.get('username'))
        return render_template('about.html', name=session.get('username'), priority=session.get('priority'))


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
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # print(request.form)
        result = opSql.register(request.form['name'], request.form['email'], request.form['pwd'])
        if result == 'success':
            return redirect(url_for('index'))
        else:
            return redirect(url_for(register))


@app.route('/news/<newsid>')
def getnews(newsid):
    content = opSql.get_new(newsid)
    imgs = opSql.get_new_img(newsid)
    if session.get('username') is None:
        return render_template('newscontent.html', title=content[1], subtitle=content[2], content=content[3], imgs=imgs)
    else:
        return render_template('newscontent.html', title=content[1], subtitle=content[2], content=content[3], imgs=imgs,
                               name=session.get('username'), priority=session.get('priority'))


@app.route('/control', methods=['POST', 'GET'])
def control():
    if request.method == 'GET':
        return render_template('control.html')
    else:
        img = request.files['file']
        dirname = opSql.insert_news(request.form, session.get('id'))
        path = "static/images/news_img/" + dirname + "/1.jpg"
        img.save(path)
        return redirect(url_for('index'))


@app.route('/delete/', methods=['POST', 'GET'])
def delete():
    news = opSql.get_all_news()
    return render_template('delete.html', resp=news)


@app.route('/delete/<newsid>', methods=['POST', 'GET'])
def delete_new(newsid):
    opSql.delete_new(newsid)
    # print(newsid)
    return redirect(url_for('delete'))


if __name__ == '__main__':
    app.run()
