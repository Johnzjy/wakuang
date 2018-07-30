'''
文件用于更新list 文件夹内的内容
code_list
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌           ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ 
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌               ▐░▌     ▐░▌               ▐░▌     
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌               ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌               ▐░▌     ▐░░░░░░░░░░░▌     ▐░▌     
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌               ▐░▌      ▀▀▀▀▀▀▀▀▀█░▌     ▐░▌     
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌               ▐░▌               ▐░▌     ▐░▌     
▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄█░█▄▄▄▄  ▄▄▄▄▄▄▄▄▄█░▌     ▐░▌     
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀      
                                                                                                        

                                                                     
'''

import datetime
import os
import sys
from contextlib import closing

import pandas as pd
import tushare as ts

sys.path.append("..")
'''
cvs 输入格式
'gbk'
pd.read_csv(path,encoding='gbk')
to_csv(path,encoding='gbk')
'''


def update_list(path=None):
    if path is None:
        path = os.path.dirname(os.getcwd()) + '\\list\\'  # 存储路径
    else:
        pass

    print('开始更新。。。。。。')
    all_datas = ts.get_industry_classified()
    all_datas = all_datas.set_index('code')
    name = all_datas.name
    name = name.sort_index()
    name.to_csv(path + 'stock_code_all.csv', encoding='gbk', header=True)
    sz = name[name.index < '100000']
    sz.to_csv(path + 'stock_code_sz.csv', encoding='gbk', header=True)
    print('深圳已经更新')
    cy = name[(name.index > '299999') & (name.index < '400000')]
    cy.to_csv(path + 'stock_code_cy.csv', encoding='gbk', header=True)
    print('创业已经更新')
    sh = name[(name.index > '599999') & (name.index < '700000')]
    sh.to_csv(path + 'stock_code_sh.csv', encoding='gbk', header=True)
    print('上海已经更新')
    c_name_cnt = all_datas.c_name.value_counts()
    c_name_list = c_name_cnt.index
    c_name_cnt = c_name_cnt.rename('count')
    c_name_cnt = c_name_cnt.rename_axis('c_name')
    c_name_cnt.to_csv(path + 'c_name.csv', encoding='utf-8', header=True)
    for c_name in c_name_list:

        c_name_code = all_datas[all_datas['c_name'] == c_name]
        c_name_code = c_name_code['name']
        c_name_code = c_name_code.sort_index()
        c_name_code = c_name_code.rename_axis('code')
        c_name_code = c_name_code.rename('name')
        c_name_code.to_csv(
            path + '%s.csv' % (c_name), encoding='gbk', header=True)
    print('更新完成！！！！')
    return True


if __name__ == "__main__":
    import os
    path = os.path.dirname(os.getcwd()) + '\\list\\'  # 存储路径
    '''
    log 设置
    '''
    today = datetime.date.today()
    update_list()
