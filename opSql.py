import pymysql
import os
import shutil
from datetime import datetime

db = pymysql.connect("49.235.51.187", "root", "123456Web%", "ympy")
cursor = db.cursor()


def login(name, pwd):
    sql = "SELECT * FROM user WHERE name = '%s'" % name
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            if str(pwd) == result[0][2]:  # 比较密码是否正确
                if result[0][4] == 1:  # 是否为管理员（1为管理员）
                    return 1, result[0][0]
                else:
                    return 0, result[0][0]
        else:
            return -1, 0
    except pymysql:
        return -1, 0


def register(name, email, pwd=123456):
    sql = "SELECT * FROM user ORDER BY id DESC"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        id = result[0][0] + 1
        sql = "INSERT INTO user VALUES (%d,'%s','%s','%s',0)" % (id, name, pwd, email)
        cursor.execute(sql)
        db.commit()
        return "success"
    except pymysql:
        return "error"


def get_new(id):
    sql = "SELECT * FROM newsinfo WHERE id = '%s'" % id
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0]
    except pymysql:
        print("get_new() error")


def get_new_img(id):
    sql = "SELECT img FROM img WHERE newsid = %s ORDER BY imgid ASC " % id
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0]
    except pymysql:
        print("get_new_img error")


def get_cover_imgs():
    sql = "SELECT img FROM img WHERE imgid = 1 ORDER BY newsid DESC "
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except pymysql:
        print("get_cover_imgs() error")


def get_all_news():
    sql = "SELECT newsinfo.*,img,user.name FROM newsinfo,img,user WHERE newsinfo.id=img.newsid and " \
          "newsinfo.userid=user.id ORDER BY newsinfo.id DESC "
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except pymysql:
        print("get_all_news() error")


def insert_news(info, userid):
    path = 'static/images/news_img/'
    sql = "SELECT NOW()"
    try:
        cursor.execute(sql)
        time = cursor.fetchall()
        newsid = str(datetime.strftime(time[0][0], '%Y%m%d%H%M')) + info['cateid'] + str(userid)
        sql = "INSERT INTO newsinfo VALUES ('%s','%s','%s','%s',%d,'%s','%s')" % (newsid, info['title'], info['subtitle'], info['content'], userid, time[0][0], info['cateid'])
        os.mkdir(path + str(newsid))
        cursor.execute(sql)
        sql = "INSERT INTO img VALUES ('%s',%d,'%s')" % (newsid, 1, str(newsid) + '/1.jpg')
        cursor.execute(sql)
        db.commit()
        return newsid
    except pymysql:
        db.rollback()
        return print("insert_news() error")


def delete_new(id):
    path = 'static/images/news_img/'
    sql = "DELETE FROM newsinfo WHERE id = '%s'" % id
    try:
        cursor.execute(sql)
        sql = "DELETE FROM img WHERE newsid = '%s'" %id
        cursor.execute(sql)
        db.commit()
        shutil.rmtree(path + str(id))
    except pymysql:
        db.rollback()
        print("delete_new() error")

'''
s = str(datetime.strftime(insert_news()[0][0], '%Y%m%d%H%M')) + '02' + str(101)
print(s)

imgs = get_cover_imgs()
for item in (news, imgs):
    print(item[0]+item[1])
news = get_all_news()
print(len(news))
re = get_new_img(20191110132902101)
print(re[0])
'''

