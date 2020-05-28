import pymysql

db = pymysql.connect("49.235.51.187", "root", "123456Web%", "ympy")
cursor = db.cursor()


def login(id, pwd):
    sql = "SELECT * FROM user WHERE id = %d" % id
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(type(result[0][1]))
        if str(pwd) == result[0][1]:
            return True
        else:
            return False
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



