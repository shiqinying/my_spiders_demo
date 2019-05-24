import pymysql

db = pymysql.connect(
    host="shiqinying.xyz", port=3306, user="root", password="root", db="spiders"
)

cursor = db.cursor()

# cursor.execute("select version()")
#
# data = cursor.fetchone()

# cursor.execute("create database spiders default character set utf8")

# sql = "create table if not exists tiam_rank (id int not null auto_increment primary key , title varchar(255) null ,name varchar(255) null ,category varchar(255), view int, href varchar(255), image varchar(255) )"

# title = ''
# name = ''
# category = ''
# view = ''
# href = ""
# image = ""
#
# sql = "insert into spiders(title,name,category,view,href,image) values (%s,%s,%s,%s,%s,%s)"
# try:
#     cursor.execute(sql, (title,name,category,view,href,image))
#     db.commit()
# except:
#     db.rollback()
#
# db.close()

data = {
    "href": "www.baidu.com",
    "image": "www.baidu.com",
    "title": "aaa",
    "view": 1000,
    "name": "一本道",
    "category": "人兽大战",
}

table = "tiam_rank"
keys = ",".join(data.keys())
values = ",".join(["%s"] * len(data))
sql = "insert ignore into {table} ({keys}) values ({values})".format(
    table=table, keys=keys, values=values
)
try:
    ret = cursor.execute(sql, tuple(data.values()))
    if ret:
        print(ret)
        print("Successful")
        db.commit()
except Exception as e:
    print("Failed")
    print(e)
    db.rollback()
db.close()
