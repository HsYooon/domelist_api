import pymysql

host = '203.245.41.222'
user = 'user'
password = 'wjdgns001!A'
db = 'domelist'

def cursor():
    print("DB Connection Start")
    connection = pymysql.connect(host = host, user= user, password = password, db = db , charset= 'utf8', autocommit=True)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return cursor

def test(cursor):
    sql = f"select * from t_siteinfo"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        print(i)

if __name__ == "__main__":
    cursor = cursor()
    test(cursor=cursor)