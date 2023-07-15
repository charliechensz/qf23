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
    volume, 交易量（手） 
    value, 交易额（亿元） 
    pre_close, 昨日收盘价格
    change, 当日收盘价 - 上个收盘价

    pct_change, 涨幅百分比
    pct_range:  振幅百分比
    st_high: 实体高点
    st_low: 实体低点
    pct_upper: 上引线百分比
    pct_down: 下引线百分比
    <!-- pct_st: -->
    pct_st_range： 实体百分比

    MA5, 收盘价的5日移动平均线 
    MA10, 
    MA20, 
    MA30, 
    MA60, 
    MA125

    MA3_pct_change；  3天平均涨幅
    MA5_pct_change；  
    MA10_pct_change； 
    MA15_pct_change； 
    MA30_pct_change； 
    
    MAX3_pct_change； 3天中的最大涨幅
    MAX5_pct_change； 
    MAX10_pct_change；   
    MAX15_pct_change；   
    MAX30_pct_change；   

    MAX3_high：        3天内最高股价
    MAX30_high：       
    MAX90_high：      

    dema, DEMA指标值 
    macd-m, MACD指标-M线，MACD;   dif = EMA(C,12)-EMA(c,26), 计算12天平均和26天平均的差
    macd-s, MACD指标-S线，singal; dea = EMA(MACD,9),计算macd9天均值
    macd-h, MACD指标-红绿柱,      MACD=(dif-dea）*2,  histogram, MACD-Signal, Color Tick; 计算macd与signal的差值

    rsi, RSI指标 
    bb-u, 布林带线上轨 
    bb-m, 布林带线中轨
    bb-l, 布林带线下轨


   xing, 是否星线， True/False

    ''' 可能mpf 需要字段 '''
    upper_lim, 涨停价格 
    lower_lim, 跌停价格 
    last_close, 昨日收盘价 
    average, 平均价 
    volrate, 交易量（手） 
    ''' end '''

## macd
- diff, macd-m, macd = 12 天 EMA - 26 天 EMA
- dea,  macd-s, signal = 9 天 MACD的EMA
- bar,  macd-h, hist = MACD - MACD signal

    EMA（12）= 前一日EMA（12）×11/13＋今日收盘价×2/13
    EMA（26）= 前一日EMA（26）×25/27＋今日收盘价×2/27
    DIFF = 今日EMA（12）- 今日EMA（26）
    DEA = 前一日DEA×8/10＋今日DIF×2/10
        BAR = 2×(DIFF－DEA)  (MACD)

## 更多库研究

- PyqtGraph ： 可以动态优化
- blitting: 


# 概念股相关

## 5G概念股分类
  df = pro.concept(src='ts')

## 取5G概念明细
  df = pro.concept_detail(id='TS2', fields='ts_code,name')
- 

# 获得股票的基本信息：

## 基础信息：股票代码、名称、上市日期、退市日期等    

    df = pro.stock_basic(exchange='', list_status='L')
    
    ts_code	   symbol	name	   area	 industry  market	list_date
    000001.SZ	000001	平安银行	深圳	银行	主板	 19910403
    industry： 行业
    market: ['主板', '中小板', '创业板', '北交所', '科创板', 'CDR']
    list_date： 上市日期

## 公司信息

    df = pro.stock_company(exchange='', ts_code='')
    
    ts_code	str	Y	股票代码
    exchange	str	Y	交易所代码 ，SSE上交所 SZSE深交所 (SZSE 2480; SSE 1945)
    chairman	str	Y	法人代表
    manager	str	Y	总经理
    secretary	str	Y	董秘
    reg_capital	float	Y	注册资本
    setup_date	str	Y	注册日期
    province	str	Y	所在省份
    city	str	Y	所在城市
    introduction	str	N	公司介绍
    website	str	Y	公司主页
    email	str	Y	电子邮件
    office	str	N	办公室
    employees	int	Y	员工人数
    main_business	str	N	主要业务及产品
    business_scope	str	N	经营范围

## 股票 - bak_basic

    df = pro.bak_basic(trade_date='20211012', 
        fields='trade_date,ts_code,name,industry,pe,pb,float_share,liquid_assets,eps,bvps,per_undp,rev_yoy,profit_yoy,gpr,npr')
    
    trade_date	str	Y	交易日期
    ts_code	str	Y	TS股票代码
    name	str	Y	股票名称
    industry	str	Y	行业
    area	str	Y	地域
    pe	float	Y	市盈率（动）
    float_share	float	Y	流通股本（亿）
    total_share	float	Y	总股本（亿）
    total_assets	float	Y	总资产（亿）
    liquid_assets	float	Y	流动资产（亿）
    fixed_assets	float	Y	固定资产（亿）
    reserved	float	Y	公积金
    reserved_pershare	float	Y	每股公积金
    eps	float	Y	每股收益
    bvps	float	Y	每股净资产
    pb	float	Y	市净率
    list_date	str	Y	上市日期
    undp	float	Y	未分配利润
    per_undp	float	Y	每股未分配利润
    rev_yoy	float	Y	收入同比（%）
    profit_yoy	float	Y	利润同比（%）
    gpr	float	Y	毛利率（%）
    npr	float	Y	净利润率（%）
    holder_num	int	Y	股东人数

## back——xxx





