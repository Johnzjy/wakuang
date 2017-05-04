import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import tqdm
import os
import sys
import datetime

sys.path.append("..")
from scr import logd

log_CYQ=logd.Logger('CYQ.log')

log_CYQ.info('%s计算筹码分布模块%s'%('='*16,'='*16))

#date='2016-12-29'

def PQ(code,date):
    
    df = ts.get_tick_data(code,date)
    price_list=df.price.value_counts()
    price_list=pd.DataFrame(price_list)

    for prc in price_list.index:
        cnt_q=df[df.price==prc].volume.sum()

        price_list.loc[prc,'count_volume']=cnt_q
    price_list=price_list.sort_index()
    
    log_CYQ.info('the code %s,has been done from %s\n'%(code,date))
    
    return price_list
'''
计算筹码分布图，根据每日换手率进行累加
参数：
返回值： pf
    -

'''

   
def CYQ(code,start,end,download= False,CYQ_rate=1,files_path='E:\\database\\'):
    
    files_path=files_path+code
    df= ts.get_hist_data(code,start,end)
    df=df.reset_index()
    df=df.sort_index(ascending= False)
   
    datas= df.set_index('date')
    cyq=PQ(code,start)
   
    i =1
    for date in tqdm.tqdm(datas.index[1:]):
        try:
            tem_cyq=PQ(code,date)
        except:
            log_CYQ.error('\n数据：%s没有计算成功'%date)
            continue
        else:
            pass
        turnover=datas.turnover[i]

        try:
            tem_cyq.count_volume=tem_cyq.count_volume-(tem_cyq.count_volume*turnover//CYQ_rate)
        except:
            log_CYQ.error('\n计算换手率：%s没有计算成功'%date)
            continue

        cyq=cyq.add(tem_cyq,fill_value=0)

        if download == True:
            
            if os.path.exists(files_path) == False: # 判断文件是不是存在
                os.mkdir(files_path)                # 创建目录
            cyq.to_csv(files_path+'/%s_to_%sCYQ.csv'%(start,date))

        i +=1
        
        print (date)
    cyq_sum= cyq.count_volume.sum()
    cyq['CYQ_PCT']=cyq.count_volume/cyq_sum*100 # 计算百分比 对统计量。
    cyq['PCT_SUM']= cyq.CYQ_PCT.cumsum()          # 计算累加 cumsun（） 计算累加
        


    return cyq

def Draw_jetton(code_j,start_j,end_j):

    df= ts.get_hist_data(code_j,start_j,end_j)
    df=df.reset_index()
    df=df.sort_index(ascending= False)
    df.date=df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    datas= df.set_index('date')
    x=CYQ(code_j,start_j,end_j,download=False,CYQ_rate=100)


    PCT50 =x[x['PCT_SUM']>=50].index[0]
    PCT20 =x[x['PCT_SUM']>=20].index[0]
    PCT80 =x[x['PCT_SUM']>=80].index[0]
    
    f1 = plt.figure(1)
    f1.suptitle('code:%s    starttime:%s    endtime:%s'%(code_j,start_j,end_j),fontsize=20, color='red')
    
    plt.subplot(131)
    plt.plot(datas.index,datas.close,linewidth=1, color='k')
    plt.plot(datas.index,datas.close*0+PCT20,ls='--',linewidth=.4, color='r')
    plt.plot(datas.index,datas.close*0+PCT50,ls='--',linewidth=.4, color='r')
    plt.plot(datas.index,datas.close*0+PCT80,ls='--',linewidth=.4, color='r')
    plt.ylim(datas.close.min(),datas.close.max())
    plt.ylabel('price')
    plt.grid(True)
    
    
    plt.subplot(132)
    plt.barh(x.index,x.count_volume,height=0.005, color='g')
    plt.plot(x.count_volume,x.index*0+PCT20,ls='--',linewidth=.4, color='r')
    plt.plot(x.count_volume,x.index*0+PCT50,ls='--',linewidth=.4, color='r')
    plt.plot(x.count_volume,x.index*0+PCT80,ls='--',linewidth=.4, color='r')
    plt.ylim(datas.close.min(),datas.close.max())
    plt.grid(True)
    
    plt.subplot(133)
    plt.plot(x.PCT_SUM,x.index,linewidth=1, color='b')
    plt.plot(x.PCT_SUM,x.index*0+PCT20,ls='--',linewidth=.4, color='r')
    plt.plot(x.PCT_SUM,x.index*0+PCT50,ls='--',linewidth=.4, color='r')
    plt.plot(x.PCT_SUM,x.index*0+PCT80,ls='--',linewidth=.4, color='r')
    plt.ylim(datas.close.min(),datas.close.max())
    plt.grid(True)



    
if __name__ == "__main__":
    code_='002758'
    start_='2017-02-06'
    end_='2017-03-01'
    log_CYQ.info('%s：from %s to %s'%(code_,start_,end_))
    Draw_jetton(code_,start_,end_)
    plt.show()

