import datetime
import time
import pymysql
from sqlalchemy import create_engine
import pandas as pd

import tushare as ts
ts.set_token('11137efdbeac800606d677871a55b3fd5aef79890c59867a8f34d03e')
pro = ts.pro_api()

from qflib import basic



# __name__是Python中一个隐含的变量它代表了模块的名字
# 只有被Python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
    print('add(1,2,3)')
