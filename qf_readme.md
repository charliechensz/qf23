# qf system

## main package:

.python3
.miniconda3
.tushare
.mplfianance
.ta-lib

## git management
- cli 外部, OK
- vscode 内部
- branch: main, xm


# 数据处理

- 数据获取
    tushare   ：['open','high','low','close','pre_close','vol',    'change', 'pct_chg',    'amount']
    mplfinance：['open','high','low','close','pre_close','volume', 'change', 'pct_change', 'value']
- 输入读取: 
    用pro_bar函数，qfq选项-前复权；
- 索引
    sort_index(ascending=True)
- 字段选择
    df=df['A', 'B', 'C']
- 字段更名
    df.columns=['A','B','C']
    df.rename( columns={'vol':'volume','pct_chg':'pct_change', 'amount':'value'}, inplace=True  )

## S2, DB结构

### tran_daily

    ts_code, 
    trade_date， 
    open: 当日开盘价 
    high, 当日最高价
    low, 当日最低价 
    close, 当日收盘价 
    pre_close, 昨日收盘价格
    change, 当日收盘价 - 上个收盘价
    pct_change, 涨幅百分比
    volume, 交易量（手） 
    value, 交易额（亿元） 

### day_zhibiao 日指标

    # basic - OK
    pct_upper:  上引线%
    pct_down:  下引线%
    pct_st_range:  实体振幅%
    pct_range:  振幅%
    st_high: 实体高点
    st_low: 实体低点
    xing: int, 是否十字星，st振幅 < 1%

    #ma - OK
    ma5, close的5日移动平均线 
    ma10, ma20, ma30, ma60, ma120, ma250

    # ma3_pct_change；  3天平均涨幅
    # max3_pct_change； 3天中的最大涨幅
    # max3_high：        3天内最高股价
    # dema, DEMA指标值 
    
    # macd - OK
    - diff, macd-m, macd = 12 天 EMA - 26 天 EMA
    - dea,  macd-s, signal = 9 天 MACD的EMA
    - bar,  macd-h, hist = MACD - MACD signal
    # histogram, MACD-Signal, Color Tick; 计算macd与signal的差值

    # jx系列：均线; xl斜率， zs站上 - ing
    - jx_days_ud60: 60线以下时开始计算天数，累计。上60后清零；== OK
    
    - jx_xl_60 : 60天线斜率 
    - jx_xl_5， 10， 20， 60， 120， 250

    - jx_zs_5: 站上5线
    - jx_zs_ : 10, 20, 60, 120, 250

    - jx_sc_5_10:
    - jx_sc_ ： 10_20， 20_60

    # lj系列：量价关系， fl放量
    lj_fl_3_5
    lj_fl_ : 5_10, 5_20, 5_60 


    # rsi, RSI指标 
    # bb-u, 布林带线上轨 
    # bb-m, 布林带线中轨
    # bb-l, 布林带线下轨





    ''' 可能mpf 需要字段 '''
    upper_lim, 涨停价格 
    lower_lim, 跌停价格 
    last_close, 昨日收盘价 
    average, 平均价 
    volrate, 交易量（手） 
    ''' end '''


## 更多库研究

- PyqtGraph ： 可以动态优化
- blitting: 


