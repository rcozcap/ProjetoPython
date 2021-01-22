import pymysql as MySQLdb

def con_shop():

    con = MySQLdb.connect(host='127.0.0.1', user='developer', passwd='1234567', db='shop')