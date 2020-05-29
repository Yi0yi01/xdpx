import pymysql
import sys
from datetime import datetime

db = pymysql.connect("49.235.51.187", "root", "123456Web%", "ympy")
cursor = db.cursor()
fp = open('static/images/2019shijiebei.jpg', encoding='UTF-8', errors='ignore')
pic = fp.read()
fp.close()
'''
try:
    sq = "INSERT INTO img VALUE ('%s',%d,'%s')" % (2020, 1, pymysql.escape_string(pic))
    cursor.execute(sq)
    db.commit()
    print("done")
except pymysql:
    print("error")
'''


try:
    sq = "SELECT img FROM img WHERE newsid = '%s'" % 2020
    cursor.execute(sq)
    img = cursor.fetchone()[0]
    fp = open('static/images/test.jpg', 'wb')
    fp.write(img)
    fp.close()
except pymysql:
    print("error")


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


def get_news(id):
    sql = "SELECT * FROM newsinfo WHERE id = %s" % id
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except pymysql:
        return "error"


def insert_news():
    sql = "SELECT NOW()"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except pymysql:
        return "error"


'''
s = str(datetime.strftime(insert_news()[0][0], '%Y%m%d%H%M')) + '02' + str(101)
print(s)
'''
