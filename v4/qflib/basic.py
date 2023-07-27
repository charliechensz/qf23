import pymysql
from sqlalchemy import create_engine 
import pandas as pd
import math

from random import randint
from qflib import basic

def engine():
    host='127.0.0.1'
    username='root'
    password='Hy_79518'
    port='3306'
    database='stock'
    return create_engine('mysql+pymysql://'+
                         username+':'+password+'@'+
                         host+':'+port+'/'+
                         database+'?charset=utf8&use_unicode=1', 
                         echo=False)
    # con_to_db = pymysql.connect(host=host, user=username, passwd=password, port=port, db=database)
    # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
    # return create_engine('mysql+pymysql://root:Hy_79518@127.0.0.1:3306/stock?charset=utf8&use_unicode=1', echo=False)

def conn(engine):
    return engine.connect()
def exec_sql(conn, sql):
    return conn.execute(sql)

def read_data(conn, sql):
    return pd.read_sql_query(sql, conn, index_col=None)

def write_data(conn, df, table, status=False, mode='append'):
    write_no = df.to_sql(table, conn, index=status, if_exists=mode, chunksize=2000) # 每次写入2000个
    return write_no

def angle2degree(angle):
    return math.atan(angle)*180/math.pi
