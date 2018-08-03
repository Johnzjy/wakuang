import sys
sys.path.append("..")
from update import stock_information as stock_info
import pandas as pd
from pyecharts import Map
import pyecharts.events as events
from pyecharts_javascripthon.dom.functions import alert

def on_click(params):
    alert(params.name)


def draw_area_map():
    df=stock_info.read_stock_inoformation_csv()
    map_values= df.area.value_counts()
    
    map_=Map("stock",width=1200, height=600)
    map_.add("",map_values.index,map_values.values , maptype='china',is_visualmap=True,visual_text_color='#000')
    map_.on(events.MOUSE_CLICK, on_click)
             
    map_.render()
if __name__ == "__main__":
    x=draw_area_map()