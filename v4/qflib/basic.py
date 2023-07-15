
# from termios import NL1
# import termios, sys

import pymysql
from sqlalchemy import create_engine 
import pandas as pd

from random import randint
from qflib import basic

def engine():
    host='127.0.0.1'
    username='root'
    password='Hy_79518'
    port=3306
    database='stock'

    # return create_engine('mysql+pymysql://username:password@host:port/database?charset=utf8&use_unicode=1', echo=False)
    return create_engine('mysql+pymysql://root:Hy_79518@127.0.0.1:3306/stock?charset=utf8&use_unicode=1', echo=False)
    # engine_qf = create_engine('mysql+pymysql://root:Hy_79518@127.0.0.1:3306/stock?charset=utf8&use_unicode=1')
    # con_to_db = pymysql.connect(host=host, user=username, passwd=password, port=port, db=database)
    # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
    # global data_dir
    # data_dir = '~/qfdata'
    # return engine

def conn(engine):
    return engine.connect()

def exec_sql(engine,sql):
    return engine.connect().execute(sql)

def read_data(engine, sql):
    df = pd.read_sql_query(sql, engine.connect(), index_col=None)
    return df

def write_data(engine, df, table, status=False, mode='append'):
    if mode in ['replace', 'append'] :
        res = df.to_sql(table, engine, index=status, if_exists=mode, chunksize=5000)


# n0、n1差值小于pct百分比，True
def dif_pct(n0, n2, pct) :
    return True if abs( (n2-n0)*100/n0 ) <= pct else False   

def dif(n0, n2) :
    return (n2-n0)*100/n0   

''' 测试 '''
def roll_dice_list(n=2):
    """摇色子 . 清单 """
    list=[]
    total = 0
    # for _ in range(n):
    for i in range(n):
        value = randint(1, 6) 
        # value = random.randint(1, 6) 
        list.append( value )
        total += value 
    return total, list



# __name__是Python中一个隐含的变量它代表了模块的名字
# 只有被Python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
    print('add(1,2,3)')
