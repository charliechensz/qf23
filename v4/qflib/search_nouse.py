import numpy as np
import pandas as pd
import random 
from importlib import reload 
import talib as ta

from importlib import reload 
from qflib import basic
reload(basic)
# reload(search)


# 函数 ：合并买卖点
def merge_actions(df):    
    return 1 if df['bt_xrds']==1 or df['bt_dtts']==1 or df['bt_qmzx']==1 or df['bt_chuizi']==1 or df['bt_zonghe']==1 or df['bt_stp']==1 else 0

''' stp - tao '''
def pingtai(df):
# df, 首日涨幅8%， 每天平均波动0.75，今日涨幅

    ''' 算法 
    - 趋势OK： 125日等都在上升，
    - 多头排列开始形成； MACD-OK；
    - 突破前高，放量、或者很快补量；
    - 逼空，股价不再下跌。
    
    - MAX30天高点和3天高点差不多；
    - 

    - 结合更多技术：之间出现过买点： 如锤子/长下引线
    '''

    days = len(df)

    for i in range(days-1, days):
        
        '''買入處理'''
        # 前3、前5、前10日平均下跌
        # buy_status = True if ( df['MA3_pct_change'][i-1] < pct_fall or df['MA5_pct_change'][i-1]<pct_fall/2 or df['MA10_pct_change'][i-1]<pct_fall/3 ) else False   

        buy_status = True 

        # 还在平台期
        if buy_status:
            buy_status = True if basic.dif_pct( df['MAX90_high'][i-30], df['MAX30_high'][i], 8) else False
        # 现在股价低于， 平台期
        # if buy_status:
        #     buy_status = True if basic.dif( df['MAX3_high'][i], df['MAX90_high'][i-37]) > 10 else False

        # 近10天存在涨停板
        if buy_status:
            buy_status = True if df['MAX10_pct_change'][i] > 9.5 else False 

        # # 每天涨幅最小值，确保在上涨途中
        # if buy_status:
        #     buy_status = True if df['MA15_pct_change'][i-1]>0 or df['MA3_pct_change'][i-1]>0 else False  
        # # 忽略每天连续上涨的类型, 如昨天涨幅小于5
        # if buy_status:
        #     buy_status = True if ( df['pct_change'][i-1] ) < 6 else False  
        # # 今天涨幅7%以上。
        # if buy_status:
        #     buy_status = True if ( df['pct_change'][i] ) > change_td else False  

        # 期间有买点，如启明之星，锤子Plus
        # if buy_status:
        #     buy_status = True if df['pct_down'][i-1] > pct_down_yt else False   
        
        # 從昨晚最低漲了 5%
        if buy_status:
            # buy_day.append( ['stp', df.index[i].to_pydatetime()] )
            df.loc[df.index[i], 'bt_pingtai'] = 1

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
    return df, buy_status


''' stp - charlie '''
def pingtai2(df):
# df, 首日涨幅8%， 每天平均波动0.75，今日涨幅

    ''' 算法 
    - 趋势OK： 125日等都在上升，
    - 多头排列开始形成； MACD-OK；
    - 突破前高，放量、或者很快补量；
    - 逼空，股价不再下跌。
    
    - MAX30天高点和3天高点差不多；
    - 

    - 结合更多技术：之间出现过买点： 如锤子/长下引线
    '''

    days = len(df)

    for i in range(days-1, days):
        
        '''買入處理'''
        # 前3、前5、前10日平均下跌
        # buy_status = True if ( df['MA3_pct_change'][i-1] < pct_fall or df['MA5_pct_change'][i-1]<pct_fall/2 or df['MA10_pct_change'][i-1]<pct_fall/3 ) else False   

        buy_status = True 

        # 还在平台期
        if buy_status:
            buy_status = True if basic.dif_pct( df['MAX90_high'][i-30], df['MAX30_high'][i], 8) else False
        # 现在股价低于， 平台期
        # if buy_status:
        #     buy_status = True if basic.dif( df['MAX3_high'][i], df['MAX90_high'][i-37]) > 10 else False

        # 近10天存在涨停板
        if buy_status:
            buy_status = True if df['MAX10_pct_change'][i] > 9.5 else False 

        # # 每天涨幅最小值，确保在上涨途中
        # if buy_status:
        #     buy_status = True if df['MA15_pct_change'][i-1]>0 or df['MA3_pct_change'][i-1]>0 else False  
        # # 忽略每天连续上涨的类型, 如昨天涨幅小于5
        # if buy_status:
        #     buy_status = True if ( df['pct_change'][i-1] ) < 6 else False  
        # # 今天涨幅7%以上。
        # if buy_status:
        #     buy_status = True if ( df['pct_change'][i] ) > change_td else False  

        # 期间有买点，如启明之星，锤子Plus
        # if buy_status:
        #     buy_status = True if df['pct_down'][i-1] > pct_down_yt else False   
        
        # 從昨晚最低漲了 5%
        if buy_status:
            # buy_day.append( ['stp', df.index[i].to_pydatetime()] )
            df.loc[df.index[i], 'bt_pingtai'] = 1

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
    return df, buy_status




''' zonghe - charlie '''
def zonghe(df, pct_fall, pct_down_yt, pct_change_td, pct_2day_range):
    # df, 前3日平均跌幅，昨日下引线，今日涨幅, 昨日今日2日振幅

    buy_day, sale_day = [],[]
    # asc， 遍历日期
    for i in range(1, len(df)):
        
        #== 買入處理
        # 前3、前5、前10日平均下跌
        buy_status = True if ( df['MA3_pct_change'][i-1] < pct_fall or df['MA5_pct_change'][i-1]<pct_fall/2 or df['MA10_pct_change'][i-1]<pct_fall/3 ) else False   

        # 昨日阴线 
        # if buy_status:
        #     buy_status = True if df['change'][i-1] < 0 else False   

        # 昨日锤子下引线 
        if buy_status:
            buy_status = True if df['pct_down'][i-1] > pct_down_yt else False   
        
        # 今日陽綫 and 中陽+
        if buy_status:
            buy_status = True if df['pct_change'][i] > pct_change_td else False   # 当日涨停大阳才考虑
        # 從昨晚最低漲了 5%
        if buy_status:
            if (df['high'][i] - df['low'][i-1])*100/df['pre_close'][i] > pct_2day_range :   # 2日振幅
                buy_day.append( ['zonghe',df.index[i].to_pydatetime()] )
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
def chuizi(df, pct_fall, pct_down_yt, pct_change_td, pct_upper_td):
    # df, 前3日平均跌幅-1.5，昨日下引线2，今日涨幅2, 今日上引线2; 
    # yt: yesterday; td: today
    # res = backtest.chuizi(df, -1.5, 3, 3, 1)   # 昨日长下引线+今日中阳+短上引线

    buy_day, sale_day = [],[]
    # asc， 遍历日期
    for i in range(1, len(df)):
        
        #== 買入處理
        # 前3、前5、前10日平均下跌 大于 输入值
        buy_status = True if ( df['MA3_pct_change'][i-1]<pct_fall or df['MA5_pct_change'][i-1]<pct_fall/2 or df['MA10_pct_change'][i-1]<pct_fall/3 ) else False   

        # 昨日锤子下引线 
        if buy_status:
            buy_status = True if df['pct_down'][i-1] > pct_down_yt else False   
        
        # 今日中陽 +， 如4%
        if buy_status:
            buy_status = True if df['pct_change'][i] > pct_change_td else False   

        # 今日短上引线， #如小于2%
        if buy_status:
            buy_status = True if df['pct_upper'][i] < pct_upper_td else False   

        # 從昨晚最低漲了 5%
        if buy_status:
            # if (df['high'][i] - df['low'][i-1])*100/df['pre_close'][i] > pct_2day_range :   # 2日振幅
            buy_day.append( ['chuizi',df.index[i].to_pydatetime()] )
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
def rmzx(df, change_new):
    buy_day = []
    sale_day = []
    # asc， 遍历日期
    df['qmzx_xing'] = 0   # 初始化：全部不为星
    for i in range(1, len(df)):
        
        # 界定当日是否星线
        if i >= 1: 
            # 实体1%以内， 且实体高点还低于昨天实体低点。
            if df['pct_st_range'][i] <= 1 and df['st_high'][i] <= df['st_low'][i-1] :
                # and df['st_high'][i] <= df['st_low'][i-1]
                df.loc[df.index[i], 'qmzx_xing'] = 1
                # df['qmzx_xing'][i] = 1
        # 买入判断：
        if i >= 2:        
            # 核心逻辑判断：昨天星线后，今天是否是大阳
            
            buy_status = True if df['qmzx_xing'][i-1] == 1 else False   # 当日涨停大阳才考虑
            if buy_status:
                buy_status = True if df['change'][i] > change_new else False   # 当日涨停大阳才考虑
            if buy_status:
                buy_day.append( ['qmzx',df.index[i].to_pydatetime()] )
                df.loc[df.index[i], 'bt_qmzx'] = 1
    return buy_day, sale_day

''' 旭日东升 '''
def xrds(df, pct_change_td):
    buy_day = []
    sale_day = []
    # asc， 遍历日期
    for i in range(1, len(df)):
        
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
                buy_day.append( ['xrds',df.index[i].to_pydatetime()] )
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
def dtts(df, pct_change_td):
# dtts(df, pct_change_td-今日涨幅)
    buy_day = []
    sale_day = []
    # 遍历每天，asc 从小到大
    for i in range(1, len(df)):

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
                buy_day.append( ['dtts', df.index[i].to_pydatetime(), df['pct_change'][i], pct_change_td] )
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



# __name__是Python中一个隐含的变量它代表了模块的名字
# 只有被Python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
    print('add(1,2,3)')
