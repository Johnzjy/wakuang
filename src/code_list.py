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
"""
import pandas as pd
import os
code_dict={'all_code':'stock_code_all',
           'sh':'stock_code_sh',
           'cy':'stock_code_cy',
           'sz':'stock_code_sz',
           }
def list_input(mode='sh'):
    if mode in code_dict.keys():
        search_file=code_dict[mode]+'.csv'
        #print (search_file)
    else:
        search_file=mode+'.csv'
    print (search_file)
    
    try:
   
        f=open('..\\list\\%s'%search_file)
        print (f)
        LIST_=pd.read_csv(f)
    except IOError:
        print('can not find files,please change mode.')
        print(os.listdir('..\\list'))
    '''
    if mode == 'sh': 
        LIST_=pd.read_csv('list/stock_code_sh.csv',encoding='gbk')
    elif mode == 'sz':
        LIST_=pd.read_csv('list/stock_code_sz.csv',encoding='gbk')
    elif mode == 'cy':
        
        LIST_=pd.read_csv('list/stock_code_cy.csv',encoding='gbk')
    else:
        pass
    '''
    if LIST_ is not None:
 #       LIST_ = LIST_.drop_duplicates('code')
        LIST_['code'] = LIST_['code'].map(lambda x:str(x).zfill(6))
    return LIST_
def list_all():
    DataFame_list = list_input('all_code')
    list_code =list(DataFame_list.code.values)
    return list_code

if __name__ == "__main__":
        print (list_all())