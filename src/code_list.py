"""
                           █████                                              
                          ░░███                                               
 █████ ███ █████  ██████   ░███ █████ █████ ████  ██████   ████████    ███████
░░███ ░███░░███  ░░░░░███  ░███░░███ ░░███ ░███  ░░░░░███ ░░███░░███  ███░░███
 ░███ ░███ ░███   ███████  ░██████░   ░███ ░███   ███████  ░███ ░███ ░███ ░███
 ░░███████████   ███░░███  ░███░░███  ░███ ░███  ███░░███  ░███ ░███ ░███ ░███
  ░░████░████   ░░████████ ████ █████ ░░████████░░████████ ████ █████░░███████
   ░░░░ ░░░░     ░░░░░░░░ ░░░░ ░░░░░   ░░░░░░░░  ░░░░░░░░ ░░░░ ░░░░░  ░░░░░███
                                                                      ███ ░███
                                                                     ░░██████ 
                                                                      ░░░░░░  

获取stock 中的code 代码
    |   get_code_list
    |   get_sh_list
    |   get_sh_list
    |   get_cyb_list
    |   list_all
"""
import pandas as pd
import os
import sys
"""
code  字典
"""
code_dict = {
    'all_code': 'stock_code_all',
    'sh': 'stock_code_sh',
    'cyb': 'stock_code_cy',
    'sz': 'stock_code_sz',
    'bg': 'stock_code_sz',
}


def get_code_list(mode='sh'):
    """
    获取stock code list
    Parameters
    ----------
    mode='sh': 有四种 
                    sh ：上海
                    sz ：深圳
                    cyb ：创业板
                    all_code : 所有
                    bg ：B股
    Returns
    -------

    """
    PATH = os.path.dirname(os.path.abspath(__file__))  #利用__file__找到当前路径
    os.chdir(PATH)
    if mode in code_dict.keys():
        search_file = code_dict[mode] + '.csv'
        #print (search_file)
    else:
        search_file = mode + '.csv'
    print(search_file)

    try:
        f = open('../list/%s' % search_file)  #获取文件

        LIST_ = pd.read_csv(f)
    except IOError:
        print('can not find files,please change mode.')
        print(os.listdir('../list'))
        return False

    if mode == 'sh':
        LIST_ = pd.read_csv('../list/stock_code_sh.csv', encoding='gbk')
    elif mode == 'sz':
        LIST_ = pd.read_csv('../list/stock_code_sz.csv', encoding='gbk')
    elif mode == 'cyb':

        LIST_ = pd.read_csv('../list/stock_code_cy.csv', encoding='gbk')
    else:
        pass

    if LIST_ is not None:
        #       LIST_ = LIST_.drop_duplicates('code')
        LIST_['code'] = LIST_['code'].map(lambda x: str(x).zfill(6))
    return LIST_


def get_sh_list():
    list_code = get_code_list('sh')
    list_code = list(list_code.code.values)
    return list_code


def get_sz_list():
    list_code = get_code_list('sz')
    list_code = list(list_code.code.values)
    return list_code


def get_cyb_list():
    list_code = get_code_list('cyb')
    list_code = list(list_code.code.values)
    return list_code


def list_all():
    list_code = get_code_list('all_code')
    list_code = list(list_code.code.values)
    return list_code


if __name__ == "__main__":
    '''
        获取全部列表
    '''
    print(list_all())
