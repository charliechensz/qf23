import datetime
import time
import pymysql
from sqlalchemy import create_engine 
import pandas as pd

import tushare as ts
ts.set_token('11137efdbeac800606d677871a55b3fd5aef79890c59867a8f34d03e')
pro = ts.pro_api()

from qflib import basic

# 获得 bak_basic
def sync_basic(engine, df, table, trade_date):
    
    sql = " delete from " + table + " where true "
    print( table, basic.exec_sql(engine, sql) )
    basic.write_data(engine, df, table, False, 'append')

def sync_moneyflow(engine, period=1):
    now = datetime.datetime.now()
    # period = 825
    for n in range(-period+1, 1):
        delta = datetime.timedelta(days=n)
        new_day = now + delta
        trade_date = new_day.strftime('%Y%m%d')
        print( trade_date, end="" )  

        # 判断当日数据是否已存在
        sql="SELECT * FROM moneyflow where trade_date='" + trade_date+ "' LIMIT 10"
        df=basic.read_data(engine, sql)
        if len(df) > 0:
            print( '  - existed' )   
        else:    
            # 读取数据
            df = pro.moneyflow(trade_date=trade_date)
            print( '  - read: ', df.shape, end="")
            if len(df) == 0:
                print( '  - no found at Tushare' )
            else:
                # 删除可能的已有数据
                # sql = "delete from moneyflow where trade_date="+trade_date
                # print( 'trade_date :', trade_date )
                # print( 'delete res: ', basic.exec_sql(engine, sql) )
                # 添加数据
                basic.write_data(engine, df, 'moneyflow', False,'append') 
                print( '  - added' )

    print('\n== moneyflow daily: OK\n')

# 获得股票日交易数据 - OK
def sync_tran_daily(engine, period=1):    
    now = datetime.datetime.now()
    # period = 1501
    for n in range(-period+1, 1):
        delta = datetime.timedelta(days=n)
        new_day = now + delta
        trade_date = new_day.strftime('%Y%m%d')
        print( trade_date, end="" )  

        # existDate = False
        sql="SELECT * FROM tran_daily where trade_date='" + trade_date+ "' LIMIT 10"
        df=basic.read_data(engine, sql)
        if len(df) > 0:
            print( '  - existed' )
        else:
            # read data
            df = pro.daily(trade_date=trade_date)
            print( '  - read: ', df.shape, end="")
            if len(df) > 0:
                # print( '  - none ')
                # 删除已有数据
                # sql = "delete from tran_daily where trade_date="+trade_date
                # print( 'trade_date :', trade_date )
                # print( 'sql: ', sql )
                # print( 'delete res: ', basic.exec_sql(engine, sql) )
                # 添加数据
                basic.write_data(engine, df, 'tran_daily', False,'append')
                print( '  - Added')
            else:    
                print( '  - none ' )
    print('\n== tran_daily: OK\n')

#取000001的前复权行情
#df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
#取000001的后复权行情
#df = ts.pro_bar(ts_code='000001.SZ', adj='hfq', start_date='20180101', end_date='20181011')


# __name__是Python中一个隐含的变量它代表了模块的名字
# 只有被Python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
    print('add(1,2,3)')
