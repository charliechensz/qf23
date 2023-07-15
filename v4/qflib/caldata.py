# %matplotlib widget
import numpy as np
import pandas as pd
import random 
from importlib import reload 
import talib as ta

# from numba import jit

# import matplotlib.pyplot as plt
# import mplfinance as mpf
# import tushare as ts
# ts.set_token('11137efdbeac800606d677871a55b3fd5aef79890c59867a8f34d03e')
# pro = ts.pro_api()


''' 数值运算 def  '''
def cal_upper(df):
    return ( df['high'] - max( df['open'], df['close'] ) ) / df['pre_close'] * 100
def cal_down(df):  
    return ( min( df['open'], df['close'] ) - df['low']  ) / df['pre_close'] * 100
def cal_range(df):  # 振幅%
    return ( df['high'] - df['low']  ) / df['pre_close'] * 100
def cal_st_high(df):  
    return df['open'] if df['open'] >= df['close'] else df['close']
def cal_st_low(df):
    return df['open'] if df['open'] < df['close'] else df['close']
def cal_st(df):  # 实体振幅
    return abs( df['open'] - df['close'] )
def cal_st_range(df):  # 实体振幅%
    return abs( df['open'] - df['close']  ) / df['pre_close'] * 100

''' 计算macd '''
# 输入df_name,算法参数。其中ewm函数算法快300-500倍
def cal_macd(dfIn, macd_way=2, ema_fast=12, ema_slow=26, dea_day=9):
    dfIn['ema_fast'], dfIn['ema_slow'] = 0.0, 0.0
    dfIn['diff'], dfIn['dea'], dfIn['bar'] = 0.0,0.0,0.0
    dfIn['ema_fast'] = dfIn['close'].ewm(span=ema_fast,     adjust=False).mean()
    dfIn['ema_slow'] = dfIn['close'].ewm(span=ema_slow,     adjust=False).mean()
    dfIn['diff'] = dfIn['ema_fast'] - dfIn['ema_slow']
    dfIn['dea'] = dfIn['diff'].ewm(span=9, adjust=False).mean()
    dfIn['bar'] = (dfIn['diff'] - dfIn['dea']) * 2
    return dfIn
    
def cal_ma(dfIn):
    dfIn['MA5'],dfIn['MA10'],dfIn['MA20'] = np.nan,np.nan,np.nan
    dfIn['MA30'],dfIn['MA48'] = np.nan,np.nan
    dfIn['MA5'] = dfIn['close'].rolling(5).mean()
    dfIn['MA10'] = dfIn['close'].rolling(10).mean()
    dfIn['MA20'] = dfIn['close'].rolling(20).mean()
    dfIn['MA30'] = dfIn['close'].rolling(30).mean()
    dfIn['MA48'] = dfIn['close'].rolling(48).mean()
    return dfIn


def add(*args):
    total = 0
    for val in args:
        total += val
    return total

# __name__是Python中一个隐含的变量它代表了模块的名字
# 只有被Python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
    print('add(1,2,3)')
