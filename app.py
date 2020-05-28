from flask import *
import opSql

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/news/')
def news():
    return render_template('news.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/matches')
def matches():
    return render_template('matches.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/news/<newsid>')
def getnews(newsid):
    result = opSql.get_news(newsid)
    return render_template('newscontent.html', title=result[0][1], content1=result[0][1], content2=result[0][2])


if __name__ == '__main__':
    app.run()
