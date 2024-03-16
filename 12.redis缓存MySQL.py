import random

import pymysql
import redis

# con = pymysql.connect(user='root',password='123456')
# con.select_db('qiku')
# cur = con.cursor()
#
# # sql = "create table comment (id int primary key not null auto_increment," \
# #       "score int default 0, " \
# #       "create_time datetime default current_timestamp)"
# # cur.execute(sql)
#
#
# # 插入一万个数据
# sql = "insert into comment (score) values (%s)"
# args = [(random.randint(1, 5),) for i in range(10000)]
# line = cur.executemany(sql, args=args)
# print("影响行数", line)
# con.commit()
#
# cur.close()
# con.close()


def get_comments_top10():
    # 首先从 redis 中尝试获取！
    client = redis.StrictRedis(password="123456", db=0)
    info = client.lrange("comment_top10", 0, 9)  # 名为comment_top10的键，值为一个列表。
    if info:
        print(f"从redis取值")
        temp = []
        for data in info:
            data = data.decode().split("-")
            temp.append((data[0], data[1]))
        datas = tuple(temp)
    else:
        print(f"从mysq取值")
        con = pymysql.connect(user="root", password="123456", database="qiku")
        cur = con.cursor()
        sql = "select id, score from comment limit 10"
        cur.execute(sql)
        datas = cur.fetchall()
        for data in datas:
            client.lpush("comment_top10", f"{data[0]}-{data[1]}")
        client.expire("comment_top10", 10)
        cur.close()
        con.close()

    client.close()
    return datas


if __name__ == '__main__':
    result = get_comments_top10()
    print(result)  # 格式是一个大元组，里面是每一个小的元组！

# ((10001, 3), (10002, 4), (10003, 4), (10004, 4), (10005, 2), (10006, 3), (10007, 4), (10008, 2), (10009, 5), (10010, 4))
