
"""WK Live:
 

Usage:
    wk -h | --help
    wk -v | --version
    wk -m | --macdsh <StockCode>
    wk -t | --test <StockCode>
    wk -i | --index <StockCode>


Tips:
    Please hit Ctrl-C on the keyborad when you want to interrupt the game live.

Arguments:
    gameNumber     The key number contact to the specific game.

Options:
    -h --help        Show this help message and exit.
    -m --macdsh    download macd for shanghai stock maket
    -t --test       test
"""
from docopt import docopt
import datetime
import os
import sys
print("the curPath path:",os.getcwd())
sys.path.append(os.getcwd())
import macd_all
import technical_indicators as ti

class WK():
    def __init__(self, **kwargs):
        self._args = kwargs
        self._namelst = []
        self._hreflst = []
        self._datalst = []
        self._currenttime="%s"%datetime.date.today()
       # self._headers = self.__headers__
        #self.get_gamelist()
    def get_command(self):
        """ 处理命令行参数 """
        if self._args.get('-m') or self._args.get('--macdsh'):
            try:
                mode_=self._args.get('<StockCode>')
                #mode_='sh'
                start_='2016-10-01'
                end_=self._currenttime
                macd_all.save_MACD_all(mode_,start_,end_)
                
            except Exception:
                print(">>  测试不通过")

        if self._args.get('-i') or self._args.get('--index'):

            code_=self._args.get('<StockCode>')

            start_='2016-10-01'
            end_=self._currenttime
            ti.index_run(code_,start_,end_)
'''

        if self._args.get('-l') or self._args.get('--list'):
            if self._namelst:
                print("\n 比赛\t\t| 比赛场次\n", "-" * 25)
                for i, v in enumerate(self._namelst):
                    print(" {}\t| {}\n".format(v, i), "-" * 25)
            else:
                print(">>  暂无比赛直播")
        if self._args.get('-w') or self._args.get('--watch'):
            try:
                self.live_game(self._hreflst[int(self._args.get('<gameNumber>'))])
            except Exception:
                print(">>  无该比赛场次文字直播")
        if self._args.get('-d') or self._args.get('--data'):
            try:
                self.show_data(self._datalst[int(self._args.get('<gameNumber>'))])
            except Exception:
                print(">>  无该比赛场次球员数据")
        if self._args.get('-n') or self._args.get('--news'):
            try:
                self.show_news(int(self._args.get('<gameNumber>')))
            except Exception:
                print(">>  无该比赛场次赛后新闻")
        if self._args.get('-s') or self._args.get('--schedule'):
            try:
                self.show_schedule()
            except Exception:
                print(">>  无法查询到比赛的赛程")
        if self._args.get('-t') or self._args.get('--test'):
            try:
                self.test(self._args.get('<StockCode>'))
            except Exception:
                print(">>  测试不通过")
 '''       
    def test(self,code):
        print(code)
        

def run_macd():
    print(os.getcwd())
def cli():
    """ 入口方法 """
    args = docopt(__doc__, version='wakuang Live 0.1')
    WK(**args).get_command()

if __name__ == '__main__':
    #cli()
    x=WK()
    x.test()
