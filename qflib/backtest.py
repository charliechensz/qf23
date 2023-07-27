from tabnanny import check
import numpy as np
import pandas as pd
import random 
from importlib import reload 
import talib as ta

# from numba import jit

# 函数 ：合并买卖点
def merge_actions(df):    
    return 1 if df['bt_xrds']==1 or df['bt_dtts']==1 or df['bt_qmzx']==1 or df['bt_chuizi']==1 or \
                df['bt_zonghe']==1 or df['bt_stp']==1 \
            else 0


'''  Charlie '''
# 穿越多均线启动法
def cydjx(df):

    ''' 算法 
    - 1个涨停板
    - 第二日高位长阴洗盘、放量2倍
    - 第三日股价回升进入第二日实体部分，短下引线 （主力认为洗盘结束）。
    - 第三日尾盘买入。
    '''
    buy_day, sale_day = [],[]
    # for i in range(len(df), len(df)):
    for i in range(len(df)-40, len(df)):
        
        # 初始化
        buy_status = True \
        if \
            df['pct_change'][i] > 0 and \
            df['open'][i] <= df['MA5'][i] and df['close'][i] > df['MA5'][i] and \
            df['open'][i] <= df['MA10'][i] and df['close'][i] > df['MA10'][i] and \
            df['open'][i] <= df['MA20'][i] and df['close'][i] > df['MA20'][i] and \
            df['open'][i] <= df['MA60'][i] and df['close'][i] > df['MA60'][i] and \
            df['diff'][i]>=0 \
        else False 
            
        if buy_status:
            buy_day.append( ['stp', df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
            df.loc[df.index[i], 'bt_stp'] = 1

    return buy_day, sale_day

# 涨停后倍量长阴法
def blcy(df):
# df, 双炮之时间间隔， 板涨幅9.9， 中间最大涨幅，


    ''' 算法 
    - 1个涨停板
    - 第二日高位长阴洗盘、放量2倍
    - 第三日股价回升进入第二日实体部分，短下引线 （主力认为洗盘结束）。
    - 第三日尾盘买入。
    '''
    buy_day, sale_day = [],[]
    # for i in range(len(df), len(df)):
    for i in range(2, len(df)):
        
        # 初始化
        buy_status = True

        # 前天涨停
        if buy_status:
            buy_status = True if ( df['pct_change'][i-2] ) >= 9.9 else False  
        # 昨日高位长阴洗盘，倍量, 无上影线
        # df['st_low'][i-1]>=df['MA5'][i-1] and \
        if buy_status:
            buy_status = True \
            if \
                df['st_high'][i-1] >= df['st_high'][i-2] and df['st_low'][i-1] < df['st_high'][i-2] and \
                df['pct_upper'][i-1]==0 and \
                df['volume'][i-1]/df['volume'][i-2]>1.5 \
            else False 
    
        # 第三日股价回升进入第二日实体部分，短下引线 （主力认为洗盘结束），无上引线。
        # and df['st_high'][i] < df['st_high'][i-2]
        # df['pct_upper'][i]<=0.3 and 
        if buy_status:
            buy_status = True if \
                df['st_high'][i] > df['st_low'][i-1]  and \
                df['pct_down'][i]==0  \
            else False  
         
        if buy_status:
            buy_day.append( ['stp', df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
            df.loc[df.index[i], 'bt_stp'] = 1

    return buy_day, sale_day

''' 提前预判双头炮 - v2 Charlie '''
def stp20(df):
# df, 双炮之时间间隔， 板涨幅9.9， 中间最大涨幅，

    ''' 算法 
    + 均线60日之上才行， 且翘头向上；
    + 三金：均线、成交量(待定)、MACD-diff > 0
    + 前5,8天涨幅大于9点 - 涨停或大阳；
    + 最近4天中，有2天星线小阳；
    + 收盘价都在大阳半阳之上；

    + 第2、3天2个小星线, 上下上引线之和 < 3，
    + 第一十个字星放量，第二个缩量；
    + 时间间隔 5-13个交易日；
    + 两个大阳之间，实体多数不超过5%个点，越小越好；
    + 小阴小阳的十日最好在双涨停实体之间

    + 热点板块；
    + 牛市或者平衡市期间更好；

    # 后续考虑：
    + 科创板的涨幅翻倍计算；

    # 4、之间出现过买点： 如锤子/长下引线
    '''
    # ban_std = 10
    buy_day, sale_day = [],[]
    # 预处理
    # df['MAX15_pct_change']=df['pct_change'].rolling(15).max()
    # df['MA15_pct_change'] =df['pct_change'].rolling(15).mean()  
    # df=df.fillna(value=0)

    # for i in range(len(df), len(df)):
    for i in range(9, len(df) - 1):
        
        '''買入處理'''
        # 前3、前5、前10日平均下跌
        # buy_status = True if ( df['MA3_pct_change'][i-1] < pct_fall or df['MA5_pct_change'][i-1]<pct_fall/2 or df['MA10_pct_change'][i-1]<pct_fall/3 ) else False   

        # 第前5天涨停
        # 涨 1 2 3 4 5
        buy_status = False
        # if df['pct_change'][i-4] > 9 and df['pct_change'][i-4] < 12 and df['pct_change'][i+1] > 9 :
        if df['pct_change'][i-4] > 9 and df['pct_change'][i-4] < 12 and df['pct_upper'][i-4] and df['pct_change'][i+1] > 9 < 2:
            # half = df['st_'][i-5] / 2
            # max_price = df['close'][i-4]*(1 + df['pct_change'][i-4]/200 )
            # min_price = df['close'][i-4]*(1 - df['pct_change'][i-4]/200 )        
            buy_status = True
            # or df['pct_change'][i-8] >= 9 else False  
  
        # 验证：
        # if buy_status:
        #     buy_status = True if df['pct_change'][i+1] > 9 else False      

        # 最近3天，2天星线；
        # if buy_status:
        #     # buy_status = True if df['xing'][i] + df['xing'][i-1] + df['xing'][i-2] + df['xing'][i-3] >= 1 else False          
        #     buy_status = True if df['xing'][i]  and \
        #             df['close'][i]>min_price   and df['close'][i]<max_price   and df['open'][i]>min_price   and df['open'][i]<max_price   and abs(df['pct_change'][i])<3 and \
        #             df['close'][i-1]>min_price and df['close'][i-1]<max_price and df['open'][i-1]>min_price and df['open'][i-1]<max_price and abs(df['pct_change'][i-1])<3 and  \
        #             df['close'][i-2]>min_price and df['close'][i-2]<max_price and df['open'][i-2]>min_price and df['open'][i-2]<max_price and abs(df['pct_change'][i-2])<3 and  \
        #             df['close'][i-3]>min_price and df['close'][i-3]<max_price and df['open'][i-3]>min_price and df['open'][i-3]<max_price and abs(df['pct_change'][i-3])<3  \
        #         else False          
                    # df['close'][i-4]>min_price and df['close'][i-4]<max_price and df['open'][i-4]>min_price and df['open'][i-4]<max_price \
            
        # if buy_status:
        #     buy_status = True if df['close'][i] > df['MA60'][i] and df['MA60'][i] > df['MA60'][i-1] and df['diff'][i] > 0 else False  

            
        # 今天小k线：小星线 
        # if buy_status:
        #     buy_status = True if df['pct_st_range'][i]<2 and df['pct_change'][i]>0 and df['volume'][i]>df['volume'][i-1] else False
            # buy_status = True if df['xing'][i] and df['pct_range'][i]<4 and df['pct_change'][i]+df['pct_change'][i-1]>-1 and df['volume'][i]<df['volume'][i-1] else False

        # 前15前内存在首次涨幅
        # if buy_status:
            # buy_status = True if ( df['MAX30_pct_change'][i-1] ) >= ban_change else False     
            # buy_status = True if ( df['MAX15_pct_change'][i-1] ) >= ban_change else False     

            # 今天涨幅7%以上。
            # 每天涨幅最小值，确保在上涨途中
            # if buy_status:
            #     buy_status = True if df['MA15_pct_change'][i-1]>0 or df['MA3_pct_change'][i-1]>0 else False  
            # 忽略每天连续上涨的类型, 如昨天涨幅小于5
            # if buy_status:
            #     buy_status = True if ( df['pct_change'][i-1] ) < 6 else False  

            # 期间有买点，如启明之星，锤子Plus
            # if buy_status:
            #     buy_status = True if df['pct_down'][i-1] > pct_down_yt else False   

        # 对(i-16, i-1)天进行分析
        # if buy_status:
            # check_xiaoyangxiaoyin = False  # 检查小阳小阴
            # for m in range(i-1, i-watch_days-1, -1):
            #     if df['pct_change'][m] >= ban_change :  # 找到首根大阳
            #         act_chang = (df['close'][i]-df['close'][m])*100/df['close'][m] # 计算双板涨幅
            #         # if act_chang < 0 or act_chang > ban_change*1: # 下跌不行，时机未到；涨幅过大不行，已经启动；
            #         # if act_chang<-ban_std/3  or act_chang>ban_std*2/3: # 两次之间涨停的振幅不能太大
            #         if act_chang<-ban_std/3  or act_chang>ban_std: # 两次之间涨停的振幅不能太大
            #             buy_status = False; break
            #         if i-1-m <= 4:   # 双涨停之间日期太近了。
            #             buy_status = False; break
            #         else:
            #             check_xiaoyangxiaoyin = True  
                # if check_xiaoyangxiaoyin:
                #     if abs(df['pct_st_range'][m]) > daily_change:   # 有长阳长阴就不符合。
                #         buy_status = False; break
        
        if buy_status:
            buy_day.append( ['stp', df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
            df.loc[df.index[i], 'bt_stp'] = 1

        #== 卖出判断：
        # 昨日陰綫
        # buy_status = True if df['change'][i-1] < 0 else False   
        # sale_status = True if df['change'][i] <= - change_new else False   # 大阴            
        # # 核心逻辑判断
        # if buy_status:
        #     # 今天实体低点低于昨天低点， 高点高于昨天高点
        #     if df['st_high'][i] < df['st_low'][i-1]:
        #         sale_day.append( ['xrds', df.index[i].to_pydatetime()] )
        #         df.loc[df.index[i], 'bt_xrds'] = -1
    return buy_day, sale_day


''' 双头炮 - tao '''
def stp(df, skip_days, ban_change, daily_change, watch_days):
# df, 板涨幅， 中间最大涨幅，

    ''' 双头炮算法 
    + 均线60日之上才行；
    + 连续出现2次过大阳，8+个点以上，最好涨停；（至少大于5%）
    + 后炮上午涨停更好；
    + 时间间隔 5-15个交易日，越长后颈越大；
    + 2根阳线接近水平状态，第二根阳线上涨不超过8个点，下跌不超过5个点。
    + 两个大阳之间，实体多数不超过5%个点，越小越好；
    + 小阴小阳的十日最好在双涨停实体之间
    + 热点板块；
    + 牛市或者平衡市期间更好；

    # 后续考虑：
    + 科创板的涨幅翻倍计算；
    + 四种变异形态；

    # 4、之间出现过买点： 如锤子/长下引线
    '''
    ban_std = 10
    buy_day, sale_day = [],[]
    # 预处理
    # df['MAX15_pct_change']=df['pct_change'].rolling(15).max()
    # df['MA15_pct_change'] =df['pct_change'].rolling(15).mean()  
    # df=df.fillna(value=0)

    # for i in range(len(df), len(df)):
    for i in range(len(df)-skip_days, len(df)):
        
        '''買入處理'''
        # 前3、前5、前10日平均下跌
        # buy_status = True if ( df['MA3_pct_change'][i-1] < pct_fall or df['MA5_pct_change'][i-1]<pct_fall/2 or df['MA10_pct_change'][i-1]<pct_fall/3 ) else False   

        # 今天涨幅OK
        buy_status = True if ( df['pct_change'][i] ) >= ban_change else False  
        # 当前股价在MA60以上，即已处于上升途中；
        if buy_status:
            buy_status = True if df['close'][i] > df['MA60'][i] and df['bar'][i] > 0 else False  
        # 排除前几天是连续上涨类型，已启动的不算。
        if buy_status:
            buy_status = True if (df['MAX3_pct_change'][i-1]) < ban_change else False  
        # 前15前内存在首次涨幅
        if buy_status:
            # buy_status = True if ( df['MAX30_pct_change'][i-1] ) >= ban_change else False     
            buy_status = True if ( df['MAX15_pct_change'][i-1] ) >= ban_change else False     

            # 今天涨幅7%以上。
            # 每天涨幅最小值，确保在上涨途中
            # if buy_status:
            #     buy_status = True if df['MA15_pct_change'][i-1]>0 or df['MA3_pct_change'][i-1]>0 else False  
            # 忽略每天连续上涨的类型, 如昨天涨幅小于5
            # if buy_status:
            #     buy_status = True if ( df['pct_change'][i-1] ) < 6 else False  

            # 期间有买点，如启明之星，锤子Plus
            # if buy_status:
            #     buy_status = True if df['pct_down'][i-1] > pct_down_yt else False   

        if buy_status:
            # 对(i-16, i-1)天进行分析
            check_xiaoyangxiaoyin = False  # 检查小阳小阴
            for m in range(i-1, i-watch_days-1, -1):
                if df['pct_change'][m] >= ban_change :  # 找到首根大阳
                    act_chang = (df['close'][i]-df['close'][m])*100/df['close'][m] # 计算双板涨幅
                    # if act_chang < 0 or act_chang > ban_change*1: # 下跌不行，时机未到；涨幅过大不行，已经启动；
                    # if act_chang<-ban_std/3  or act_chang>ban_std*2/3: # 两次之间涨停的振幅不能太大
                    if act_chang<-ban_std/3  or act_chang>ban_std: # 两次之间涨停的振幅不能太大
                        buy_status = False; break
                    if i-1-m <= 4:   # 双涨停之间日期太近了。
                        buy_status = False; break
                    else:
                        check_xiaoyangxiaoyin = True  
                # if check_xiaoyangxiaoyin:
                #     if abs(df['pct_st_range'][m]) > daily_change:   # 有长阳长阴就不符合。
                #         buy_status = False; break
        
        # 從昨晚最低漲了 5%
        if buy_status:
            buy_day.append( ['stp', df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
            df.loc[df.index[i], 'bt_stp'] = 1

        #== 卖出判断：
        # 昨日陰綫
        # buy_status = True if df['change'][i-1] < 0 else False   
        # sale_status = True if df['change'][i] <= - change_new else False   # 大阴            
        # # 核心逻辑判断
        # if buy_status:
        #     # 今天实体低点低于昨天低点， 高点高于昨天高点
        #     if df['st_high'][i] < df['st_low'][i-1]:
        #         sale_day.append( ['xrds', df.index[i].to_pydatetime()] )
        #         df.loc[df.index[i], 'bt_xrds'] = -1
    return buy_day, sale_day

''' zonghe - charlie '''
def zonghe(df, skip_days,pct_fall, pct_down_yt, pct_change_td, pct_2day_range):
    # df, 前算天数，前3日平均跌幅，昨日下引线，今日涨幅, 昨日今日2日振幅

    buy_day, sale_day = [],[]
    # asc， 遍历日期
    for i in range(len(df)-skip_days, len(df)):
        
        #== 買入處理
        buy_status = True

        # 前3、前5、前10日平均下跌
        # buy_status = True if ( df['MA3_pct_change'][i-1] < pct_fall or df['MA5_pct_change'][i-1]<pct_fall/2 or df['MA10_pct_change'][i-1]<pct_fall/3 ) else False   

        # 昨日阴线 
        # if buy_status:
        #     buy_status = True if df['change'][i-1] < 0 else False   

        # 前10有大阳线, 且高于今天，即还未启动
        if buy_status:
            buy_status = True if df['MAX10_pct_change'][i-1] > 8 and \
                df['MAX10_pct_change'][i-1] > df['close'][i] \
                else False   

        half_qmzx = False
        if half_qmzx :
            # 今天是锤子，有下引线 
            if buy_status:
                buy_status = True if df['pct_down'][i] > 1 else False   
                # buy_status = True if df['pct_down'][i] > pct_down_yt else False   

            # 今天是星线 
            if buy_status:
                buy_status = True if df['pct_st_range'][i] <= 1 else False   
                # buy_status = True if df['pct_down'][i] > pct_down_yt else False   
        else:
            if buy_status:
                buy_status = True if \
                    df['pct_down'][i-1] > 1 and df['pct_st_range'][i-1] <= 1.5 \
                    else False
                    # df['pct_change'][i] >= 1 \
                    # df['st_low'][i-2] > df['st_high'][i-1] and \

        # 昨天和今天可能构成启明星
        if buy_status:
            # buy_status = True if df['pct_down'][i] > 2 else False   
            buy_status = True if df['st_low'][i-1] > df['st_high'][i] else False   
        
        # 今日陽綫 and 中陽+
        # if buy_status:
        #     buy_status = True if df['pct_change'][i] > pct_change_td else False   # 当日涨停大阳才考虑

        # 從昨晚最低漲了 5%
        # if buy_status:
        #     # 2日振幅
        #     buy_status = True if (df['high'][i] - df['low'][i-1])*100/df['pre_close'][i] > pct_2day_range else False   
        
        if buy_status:
                buy_day.append( ['zonghe',df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
                df.loc[df.index[i], 'bt_zonghe'] = 1

        #== 卖出判断：
        # 昨日陰綫
        # buy_status = True if df['change'][i-1] < 0 else False   
        # sale_status = True if df['change'][i] <= - change_new else False   # 大阴            
        # # 核心逻辑判断
        # if buy_status:
        #     # 今天实体低点低于昨天低点， 高点高于昨天高点
        #     if df['st_high'][i] < df['st_low'][i-1]:
        #         sale_day.append( ['xrds', df.index[i].to_pydatetime()] )
        #         df.loc[df.index[i], 'bt_xrds'] = -1
    return buy_day, sale_day

''' 锤子Plus '''
# @jit(nopython=True)
def chuizi(df, skip_days, pct_fall, pct_down_yt, pct_change_td, pct_upper_td):
    # df, 前3/5/10日平均跌幅>1，昨日下引线>5，今日涨幅>2, 今日上引线<1
    # yt: yesterday; td: today
    # res = backtest.chuizi(df, -1.5, 3, 3, 1)   # 昨日长下引线+今日中阳+短上引线

    buy_day, sale_day = [],[]
    # asc， 遍历日期
    for i in range(len(df)-skip_days, len(df)):
        
        #== 買入處理
        buy_status = True
        
        # 前3、前5、前10日平均下跌 大于 输入值
        # buy_status = True if ( df['MA3_pct_change'][i-1]<pct_fall or \
        #     df['MA5_pct_change'][i-1]<pct_fall or \
        #     df['MA10_pct_change'][i-1]<pct_fall ) \
        #     else False   

        # 昨日锤子下引线：长，如4-5 
        if buy_status:
            buy_status = True if df['pct_down'][i-1] > pct_down_yt else False   
        
        # 今日阳线，中等，如2-4%
        if buy_status:
            buy_status = True if df['pct_change'][i] > pct_change_td else False   

        # # 今日上引线，短，如小于2%
        if buy_status:
            buy_status = True if df['pct_upper'][i] < pct_upper_td else False   
        # # 從昨晚最低漲了 5%
        if buy_status:
            # if (df['high'][i] - df['low'][i-1])*100/df['pre_close'][i] > pct_2day_range :   # 2日振幅
            buy_day.append( ['chuizi',df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
            df.loc[df.index[i], 'bt_chuizi'] = 1
                
        #== 卖出判断：
        # 昨日陰綫
        # buy_status = True if df['change'][i-1] < 0 else False   
        # sale_status = True if df['change'][i] <= - change_new else False   # 大阴            
        # # 核心逻辑判断
        # if buy_status:
        #     # 今天实体低点低于昨天低点， 高点高于昨天高点
        #     if df['st_high'][i] < df['st_low'][i-1]:
        #         sale_day.append( ['xrds', df.index[i].to_pydatetime()] )
        #         df.loc[df.index[i], 'bt_xrds'] = -1
    return buy_day, sale_day

''' 启明之星 '''
def qmzx(df, skip_days,pct_change_td):
    buy_day = []
    sale_day = []
    # asc， 遍历日期
    df['qmzx_xing'] = 0   # 初始化：全部不为星
    for i in range(len(df)-skip_days, len(df)):
        
        # 界定当日是否星线: 实体1%以内， 且实体高点还低于昨天实体低点。
        if df['pct_st_range'][i] <= 1 and df['st_high'][i] <= df['st_low'][i-1] :
            df.loc[df.index[i], 'qmzx_xing'] = 1
            # df['qmzx_xing'][i] = 1
            df.loc[df.index[i], 'qmzx_xing'] = 1

        # 买入判断：核心逻辑判断：昨天星线后，今天是否是大阳
        # 昨天是星线
        buy_status = True if df['qmzx_xing'][i-1] == 1 else False   
        if buy_status:
            # 当日涨停大阳
            buy_status = True if df['change'][i] > pct_change_td else False   
        if buy_status:
            buy_day.append( ['qmzx',df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
            df.loc[df.index[i], 'bt_qmzx'] = 1
    return buy_day, sale_day

''' 旭日东升 '''
def xrds(df, skip_days, pct_change_td):
    buy_day = []
    sale_day = []
    # asc， 遍历日期
    day_from = min( 1, len(df)-skip_days )
    for i in range( day_from, len(df)):
        
        #== 買入處理
        # 前3日下跌通道 / 平均
        buy_status = True if ( df['MA5_pct_change'][i-1] < -1 or df['MA3_pct_change'][i-1] < -1 ) else False   
        # 昨日阴线 
        if buy_status:
            buy_status = True if df['pct_change'][i-1] < 0 else False   
        # 今日陽綫 and 中陽+
        if buy_status:
            buy_status = True if df['pct_change'][i] > pct_change_td else False   # 当日涨停大阳才考虑
        # 高開、高走，超過昨天st高點
        if buy_status:
            if df['open'][i] > df['close'][i-1] and df['close'][i] > df['open'][i-1] :
                buy_day.append( ['xrds',df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
                df.loc[df.index[i], 'bt_xrds'] = 1

        #== 卖出判断：
        # 昨日陰綫
        # buy_status = True if df['change'][i-1] < 0 else False   
        # sale_status = True if df['change'][i] <= - pct_change_td else False   # 大阴            
        # # 核心逻辑判断
        # if buy_status:
        #     # 今天实体低点低于昨天低点， 高点高于昨天高点
        #     if df['st_high'][i] < df['st_low'][i-1]:
        #         sale_day.append( ['xrds', df.index[i].to_pydatetime()] )
        #         df.loc[df.index[i], 'bt_xrds'] = -1
    return buy_day, sale_day

''' 多头吞噬 '''
def dtts(df,skip_days, pct_change_td):
# dtts(df, pct_change_td-今日涨幅)
    buy_day = []
    sale_day = []
    # 遍历每天，asc 从小到大
    for i in range(len(df)-skip_days, len(df)):

        ''' 买入判断 '''
        # 今天阳线、昨天阴线
        buy_status = True if df['pct_change'][i] > 0 and df['pct_change'][-i] <= 0 else False
        # 今日涨幅
        if buy_status:
            buy_status = True if df['pct_change'][i] >= pct_change_td else False
                
        # 核心逻辑判断
        if buy_status:
            # 今天实体低点低于昨天低点， 高点高于昨天高点
            if df['st_low'][i] <= df['st_low'][i-1] and df['st_high'][i] > df['st_high'][i-1]:
                buy_day.append( ['dtts', df.index[i].to_pydatetime().strftime('%Y-%m-%d')] )
                df.loc[df.index[i], 'bt_dtts'] = 1

        ''' 卖出判断 '''
        # 昨天阳线、且今天阴线
        # if df['change'][i] < 0 and df['change'][-i] >= 0:
        #     sale_status = True
        # else:
        #     sale_status = False
        # # 实体波幅判断
        # if sale_status:  
        #     if abs(df['pct_change'][i]) < change_new:
        #         sale_status = False
        # # 核心逻辑判断
        # if sale_status:
        #     # 今天实体高点高于昨天高点， 低点低于昨天低点
        #     if df['st_high'][i] >= df['st_high'][i-1] and df['st_low'][i] < df['st_low'][i-1]:
        #         sale_day.append( ['dtts', df.index[i].to_pydatetime()] )
        #         df.loc[df.index[i], 'bt_dtts'] = -1
    return buy_day, sale_day

# 函数 - 计算收益
def bt_profit(df, df_bt):
    open_money = 10_0000.0
    balance = open_money
    money_OK = True
    sum_profit = 0
    stock_num = 0

    # 初始化bt_log
    bt_log = pd.DataFrame(columns=[ 'date','action','price','stock_num','money','balance','unit_profit','sum_profit','pct_profit'])
    for i in range(0, df_bt.shape[0] ):
        # price = df.iloc[lambda x: x.index == df_act.index[i]]['open'][0]
        price = df.loc[ df_bt.index[i], 'open']
        #       df.loc[ df.index[1] , 'open']

        if (df_bt['bt_s1'][i] == 1) & money_OK==True:
            # & money_OK==True
            money_OK = False
            buy_price = price
            stock_num = int( balance / buy_price )
            buy_money = stock_num*buy_price
            balance -= buy_money

            line1 = pd.Series({'date':df_bt.index[i], 'action':'buy', 'price':buy_price, 'stock_num':stock_num, 'money':buy_money , 'balance':balance,'unit_profit':0, 'sum_profit':0})
            bt_log = bt_log.append(line1, ignore_index=True)
            # print(df_act.index[i], 'to buy: ', buy_price, own_num, buy_money, money_exist)

        if (df_bt['bt_s1'][i] == -1) & (stock_num != 0):
            money_OK = True
            sale_price = price
            unit_profit = sale_price - buy_price
            balance += stock_num * price 
            sum_profit += unit_profit * stock_num
            stock_num = 0
            pct_profit = sum_profit/open_money*100

            line2 = pd.Series({'date':df_bt.index[i],'action':'sale', 'price':round(sale_price,2), 
                'stock_num':round(stock_num), 'money':round(sale_price*stock_num,2), 
                'balance':round(balance,2), 'unit_profit':round(unit_profit,2), 
                'sum_profit':round(sum_profit,2), 'pct_profit':round(pct_profit,2)})
            bt_log = bt_log.append(line2, ignore_index=True)
            # print(df_act.index[i], 'to sale: ', sale_price, unit_profit, money_exist, sum_profit)

    if stock_num != 0:
        price = df.loc[ df.index[-1], 'open']
        balance += stock_num * price
        unit_price = price - buy_price
        sum_profit += (price - buy_price) * stock_num
        pct_profit = sum_profit/open_money*100

        line2 = pd.Series({'date':df.index[-1],'action':'sale', 'price':round(price,2), 
            'stock_num':round(stock_num,0), 'money':round(price*stock_num,2), 
            'balance':round(balance,2),'unit_profit':round(unit_profit,2),
            'sum_profit':round(sum_profit,2), 'pct_profit':round(pct_profit,2)})
        bt_log = bt_log.append(line2, ignore_index=True)

    return bt_log   



# __name__是Python中一个隐含的变量它代表了模块的名字
# 只有被Python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
    print('add(1,2,3)')
