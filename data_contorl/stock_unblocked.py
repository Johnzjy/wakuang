import pandas as pd
import tushare as ts
import time
import sys
import tqdm 

print ()
sys.path.append("..")
from scr import logd
logger=logd.Logger('../scr/logfiles.log')
get_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
today=time.strftime("%Y-%m-%d", time.localtime())


class unblock(object):
    def __init__(self):
        #self.during=12
        logger.info('%s股票解禁（万股）-stock unblocked%s'%('='*8,'='*8))
    def update_unblocked(self,during=12):
        self.during=during
        logger.info(get_time)
        logger.info('update unblocked stock %s months'%self.during)
        month=int(time.strftime("%m", time.localtime()))
        year=int(time.strftime("%Y", time.localtime()))
        df=pd.DataFrame()
        
        for i in range(0,self.during):
            if month > 12:
                year +=1
                month=1
            
            logger.debug('search the %s-%s datas'%(year,month))
            try:
                temp=ts.xsg_data(year=year,month=month)
                df=df.append(temp,ignore_index=True)
            except:
                logger.error('this month data error')
                pass
            month +=1
        #df=df.reset_index()
        logger.info('downloading_completed')
        return df
    
 
    def downloading_unblocked(self,during=12,save=True):
        datas=self.update_unblocked(during)
        if save == True:
            logger.info("saving .....")
            datas.to_csv("../report/unblock/%s_stock_unblocked_%smonth.csv"%(today,during))
            logger.info("can check   ../report/unblock/%s_stock_unblocked_%smonth.csv"%(today,during))
            
        else:
            logger.error('save is not TRUE')
    
    def search_stock(self,code_='300226',during=12):
        #寻找一年以内是否有大额解禁。
        #通过网络实现，数据库为建立
        datas=self.update_unblocked(during)
        
        if code_ in datas['code'].values:
            logger.info("find %s unblocked in the next %s month!!!"%(code_,during))
            code_info=datas[datas['code']=='%s'%code_]
        else:
            logger.info("%s not find unblocked ,its safe."%code_)
            code_info=0
        return code_info
    def sum_unblocked(self,during=1):
        datas=self.update_unblocked(during)
        datas['amount_ma20']=0.0
        print (datas)
        for code_ in tqdm.tqdm(datas['code']):
            item_= list(datas['code']).index(code_) # 寻找坐标
            hist_data=ts.get_realtime_quotes(code_)
            price=hist_data.price
            print (price)
            count_=datas.at[item_,'count']
  #          print(datas.at[item_,'amount_ma20'],count_.type(),price)
            datas.at[item_,'funds']=float(count_)*float(price)#单位万元
        print(datas)
      
            
            
        
        
    
    
x=unblock()
y=x.sum_unblocked()