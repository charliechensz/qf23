
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




