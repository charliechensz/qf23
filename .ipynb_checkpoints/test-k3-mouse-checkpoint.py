# import matplotlib.pyplot as plt
import tushare as ts
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %matplotlib inline
# import matplotlib
# matplotlib.use('TkAgg')    // 解决backend non-gui 的问题
# import matplotlib.pyplot
# from matplotlib.font_manager import FontProperties

ts.set_token('11137efdbeac800606d677871a55b3fd5aef79890c59867a8f34d03e')
pro = ts.pro_api()

# from matplotlib.dates import date2num
# from cycler import cycler
# font = FontProperties(fname="SimHei.ttf", size=14)

# Part 1
# -----------------
daily = ts.pro_bar('000001.SZ', start_date='2019-01-01', end_date='20191231')
# daily.info()
daily.index = daily.trade_date

# 这些数据的Index并不是时间序列，交易日期是以字符串的形式存储在trade_date列中的，需要将日期作为DataFrame的Index，并把它们转化为pandas.Timestamp格式。
daily = daily.rename(index=pd.Timestamp)
daily_all = daily
daily.head(3)

# 删除不需要的column
daily.drop(columns=['ts_code', 'trade_date', 'pre_close',
    'change', 'pct_chg', 'amount'], inplace=True)
# 修改Column名字
daily.columns = ['open', 'high', 'low', 'close', 'volume']
daily.sort_index(inplace=True)
daily.head(3)
# mpf.plot(daily[0:50], type='candle', volume=True, style='charles',
#          mav=(5, 10, 20, 30), figratio=(16, 9), figscale=1.2)

# 符合中国习惯的配色风格——红涨绿跌自然是必须实现的第一步
# 图表上要能显示股票代码和股票名称、以及价格信息
# 图表上要显示完整的移动平均线
# 在交易量的下方显示第三张图表，同步显示相关指标如MACD等
# 在图表上用鼠标单击拖动，可以平移K线图以显示更早或更晚的K线
# 在图表上是用鼠标滚轮缩放，可以实现放大或缩小所显示的K线的范围
# 在图表上双击，可以循环切换移动平均线和布林带线
# 在指标图上双击，可以循环切换不同的指标类型如MACD/DEMA/RSI等等

# Part 2
# ==================
# 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
my_color = mpf.make_marketcolors(up='r',
                                 down='g',
                                 edge='inherit',
                                 wick='inherit',
                                 volume='inherit')
# 设置图表的背景色
my_style = mpf.make_mpf_style(marketcolors=my_color,
                              figcolor='(0.82, 0.83, 0.85)',
                              gridcolor='(0.82, 0.83, 0.85)')

# 读取测试数据
data = pd.read_csv('test_data.csv', index_col=0)
# data = pd.read_csv('test_data.csv', index_col=0).sort_index(ascending=True)
# data.head(3)
data.index = pd.to_datetime(data.index)
data.head(3)
# data.shape
# data.index[0:15]
# data.info(all)

# 读取的测试数据索引为字符串类型，需要转化为时间日期类型

mpf.plot(data.iloc[50:200], style=my_style, type='candle', volume=True, mav=(
    5, 10, 20, 30), figratio=(16, 9), figscale=1.2)


# # data是测试数据，可以直接下载后读取，在下例中只显示其中100个交易日的数据
# plot_data = data.iloc[100: 200]
# plot_data.head(3)
# # 读取显示区间最后一个交易日的数据
# last_data = plot_data.iloc[-1]
# last_data

# 标题格式，字体为中文字体，颜色为黑色，粗体，水平中心对齐
title_font = {'fontname': 'pingfang HK',
              'size':     '16',
              'color':    'black',
              'weight':   'bold',
              'va':       'bottom',
              'ha':       'center'}
# 红色数字格式（显示开盘收盘价）粗体红色24号字
large_red_font = {'fontname': 'Arial',
                  'size':     '24',
                  'color':    'red',
                  'weight':   'bold',
                  'va':       'bottom'}
# 绿色数字格式（显示开盘收盘价）粗体绿色24号字
large_green_font = {'fontname': 'Arial',
                    'size':     '24',
                    'color':    'green',
                    'weight':   'bold',
                    'va':       'bottom'}
# 小数字格式（显示其他价格信息）粗体红色12号字
small_red_font = {'fontname': 'Arial',
                  'size':     '12',
                  'color':    'red',
                  'weight':   'bold',
                  'va':       'bottom'}
# 小数字格式（显示其他价格信息）粗体绿色12号字
small_green_font = {'fontname': 'Arial',
                    'size':     '12',
                    'color':    'green',
                    'weight':   'bold',
                    'va':       'bottom'}
# 标签格式，可以显示中文，普通黑色12号字
normal_label_font = {'fontname': 'pingfang HK',
                     'size':     '12',
                     'color':    'black',
                     'va':       'bottom',
                     'ha':       'right'}
# 普通文本格式，普通黑色12号字
normal_font = {'fontname': 'Arial',
               'size':     '12',
               'color':    'black',
               'va':       'bottom',
               'ha':       'left'}


class InterCandle:  # 定义一个交互K线图类
    def __init__(self, data, my_style):

        # 鼠标按键状态，False为按键未按下，True为按键按下
        self.press = False
        # 鼠标按下时的x坐标
        self.xpress = None
        # 鼠标滚动处理
        self.idx_range = 100  # 控制K线图的显示范围大小

        # 初始化交互式K线图对象，历史数据作为唯一的参数用于初始化对象
        self.data = data
        self.style = my_style
        # 设置初始化的K线图显示区间起点为0，即显示第0到第99个交易日的数据（前100个数据）
        self.idx_start = 0

        # 初始化figure对象，在figure上建立三个Axes对象并分别设置好它们的位置和基本属性
        self.fig = mpf.figure(style=my_style, figsize=(
            12, 8), facecolor=(0.82, 0.83, 0.85))
        fig = self.fig

        # 鼠标按下事件与self.on_press回调函数绑定
        fig.canvas.mpl_connect('button_press_event', self.on_press)
        # 鼠标按键释放事件与self.on_release回调函数绑定
        fig.canvas.mpl_connect('button_release_event', self.on_release)
        # 鼠标移动事件与self.on_motion回调函数绑定
        fig.canvas.mpl_connect('motion__notify_event', self.on_motion)
        # 将新增的回调函数on_scroll与鼠标滚轮事件绑定起来
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)

        self.ax1 = fig.add_axes([0.08, 0.25, 0.88, 0.60])
        self.ax2 = fig.add_axes([0.08, 0.15, 0.88, 0.10], sharex=self.ax1)
        self.ax2.set_ylabel('volume')
        self.ax3 = fig.add_axes([0.08, 0.05, 0.88, 0.10], sharex=self.ax1)
        self.ax3.set_ylabel('macd')
        # 初始化figure对象，在figure上预先放置文本并设置格式，文本内容根据需要显示的数据实时更新
        # 初始化时，所有的价格数据都显示为空字符串
        self.t1 = fig.text(0.50, 0.94, 'TITLE', **title_font)
        self.t2 = fig.text(0.12, 0.90, '开/收: ', **normal_label_font)
        self.t3 = fig.text(0.14, 0.89, '', **large_red_font)
        self.t4 = fig.text(0.14, 0.86, '', **small_red_font)
        self.t5 = fig.text(0.22, 0.86, '', **small_red_font)
        self.t6 = fig.text(0.12, 0.86, '', **normal_label_font)
        self.t7 = fig.text(0.40, 0.90, '高: ', **normal_label_font)
        self.t8 = fig.text(0.40, 0.90, '', **small_red_font)
        self.t9 = fig.text(0.40, 0.86, '低: ', **normal_label_font)
        self.t10 = fig.text(0.40, 0.86, '', **small_green_font)
        self.t11 = fig.text(0.55, 0.90, '量(万手): ', **normal_label_font)
        self.t12 = fig.text(0.55, 0.90, '', **normal_font)
        self.t13 = fig.text(0.55, 0.86, '额(亿元): ', **normal_label_font)
        self.t14 = fig.text(0.55, 0.86, '', **normal_font)
        self.t15 = fig.text(0.70, 0.90, '涨停: ', **normal_label_font)
        self.t16 = fig.text(0.70, 0.90, '', **small_red_font)
        self.t17 = fig.text(0.70, 0.86, '跌停: ', **normal_label_font)
        self.t18 = fig.text(0.70, 0.86, '', **small_green_font)
        self.t19 = fig.text(0.85, 0.90, '均价: ', **normal_label_font)
        self.t20 = fig.text(0.85, 0.90, '', **normal_font)
        self.t21 = fig.text(0.85, 0.86, '昨收: ', **normal_label_font)
        self.t22 = fig.text(0.85, 0.86, '', **normal_font)

    def refresh_plot(self, idx_start):
        """ 根据最新的参数，重新绘制整个图表
        """
        all_data = self.data
        plot_data = all_data.iloc[idx_start: idx_start + 100]

        ap = []
        # 添加K线图重叠均线
        ap.append(mpf.make_addplot(
            plot_data[['MA5', 'MA10', 'MA20', 'MA60']], ax=self.ax1))
        # 添加指标MACD
        ap.append(mpf.make_addplot(
            plot_data[['macd-m', 'macd-s']], ax=self.ax3))
        bar_r = np.where(plot_data['macd-h'] > 0, plot_data['macd-h'], 0)
        bar_g = np.where(plot_data['macd-h'] <= 0, plot_data['macd-h'], 0)
        ap.append(mpf.make_addplot(
            bar_r, type='bar', color='red', ax=self.ax3))
        ap.append(mpf.make_addplot(
            bar_g, type='bar', color='green', ax=self.ax3))
        # 绘制图表
        mpf.plot(plot_data,
            ax=self.ax1,
            volume=self.ax2,
            addplot=ap,
            type='candle',
            style=self.style,
            datetime_format='%Y-%m',
            xrotation=0)
        self.fig.show()

    def refresh_texts(self, display_data):
        """ 
            更新K线图上的价格文本
        """
        # display_data是一个交易日内的所有数据，将这些数据分别填入figure对象上的文本中
        self.t3.set_text(
            f'{np.round(display_data["open"], 3)} / {np.round(display_data["close"], 3)}')
        self.t4.set_text(f'{display_data["change"]}')
        self.t5.set_text(f'[{np.round(display_data["pct_change"], 2)}%]')
        self.t6.set_text(f'{display_data.name.date()}')
        self.t8.set_text(f'{display_data["high"]}')
        self.t10.set_text(f'{display_data["low"]}')
        self.t12.set_text(f'{np.round(display_data["volume"] / 10000, 3)}')
        self.t14.set_text(f'{display_data["value"]}')
        self.t16.set_text(f'{display_data["upper_lim"]}')
        self.t18.set_text(f'{display_data["lower_lim"]}')
        self.t20.set_text(f'{np.round(display_data["average"], 3)}')
        self.t22.set_text(f'{display_data["last_close"]}')
        # 根据本交易日的价格变动值确定开盘价、收盘价的显示颜色
        if display_data['change'] > 0:  # 如果今日变动额大于0，即今天价格高于昨天，今天价格显示为红色
            close_number_color = 'red'
        elif display_data['change'] < 0:  # 如果今日变动额小于0，即今天价格低于昨天，今天价格显示为绿色
            close_number_color = 'green'
        else:
            close_number_color = 'black'
        self.t1.set_color(close_number_color)
        self.t2.set_color(close_number_color)
        self.t3.set_color(close_number_color)

    def on_press(self, event):
        # 当鼠标按键按下时，调用该函数，event为事件信息，是一个dict对象，包含事件相关的信息
        # 如坐标、按键类型、是否在某个Axes对象内等等
        # event.inaxes可用于判断事件发生时，鼠标是否在某个Axes内，在这里我们指定，只有鼠
        # 标在ax1内时，才能平移K线图，否则就退出事件处理函数
        print(event.inaxes)
        if not event.inaxes == self.ax1:
            return
        # 检查是否按下了鼠标左键，如果不是左键，同样退出事件处理函数
        if event.button != 1:
            return
        # 如果鼠标在ax1范围内，且按下了左键，条件满足，设置鼠标状态为pressed
        self.pressed = True
        # 同时记录鼠标按下时的x坐标，退出函数，等待鼠标移动事件发生
        self.xpress = event.xdata
        print(self.xpress)

	# 鼠标移动事件处理
    def on_motion(self, event):
        # 如果鼠标按键没有按下pressed == False，则什么都不做，退出处理函数
        if not self.pressed:
            return
        # 如果移动出了ax1的范围，也退出处理函数
        if not event.inaxes == self.ax1:
            return
        # 如果鼠标在ax1范围内，且左键按下，则开始计算dx，并根据dx计算新的K线图起点
        dx = int(event.xdata - self.xpress)
        # 前面介绍过了，新的起点N(new) = N - dx
        new_start = self.idx_start - dx
        # 设定平移的左右界限，如果平移后超出界限，则不再平移
        if new_start <= 0:
            new_start = 0
        if new_start >= len(self.data) - 100:
            new_start = len(self.data) - 100

        # 清除各个图表Axes中的内容，准备以新的起点重新绘制
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        # 更新图表上的文字、以新的起点开始绘制K线图
        self.refresh_texts(self.data.iloc[new_start])
        self.refresh_plot(new_start)

	# 鼠标按键释放
    def on_release(self, event):
        # 按键释放后，设置鼠标的pressed为False
        self.pressed = False
        # 此时别忘了最后一次更新K线图的起点，否则下次拖拽的时候就不会从这次的起点开始移动了
        dx = int(event.xdata - self.xpress)
        self.idx_start -= dx
        print(self.idx_start)
        if self.idx_start <= 0:
            self.idx_start = 0
        if self.idx_start >= len(self.data) - 100:
            self.idx_start = len(self.data) - 100

    # 鼠标滚动的处理
    def on_scroll(self, event):
        # 仅当鼠标滚轮在axes1范围内滚动时起作用
        if event.inaxes != self.ax1:
            return
        if event.button == 'down':
            # 缩小20%显示范围
            scale_factor = 0.8
        if event.button == 'up':
            # 放大20%显示范围
            scale_factor = 1.2
	# 设置K线的显示范围大小
        self.idx_range = int(self.idx_range * scale_factor)
        # 限定可以显示的K线图的范围，最少不能少于30个交易日，最大不能超过当前位置与
        # K线数据总长度的差
        data_length = len(self.data)
        if self.idx_range >= data_length - self.idx_start:
            self.idx_range = data_length - self.idx_start
        if self.idx_range <= 30:
            self.idx_range = 30
	# 更新图表（注意因为多了一个参数idx_range，refresh_plot函数也有所改动）
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.refresh_texts(self.data.iloc[self.idx_start])
        self.refresh_plot(self.idx_start, self.idx_range)

from_num = 101
candle = InterCandle(data, my_style)
candle.refresh_texts(data.iloc[from_num])
candle.refresh_plot(from_num)
# fig.show()
