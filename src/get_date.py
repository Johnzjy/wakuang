import datetime


def get_quarter(startdate=None,enddate=None):
    """
    docstring here
        :param startdate=None: 开始时间 str
        :param enddate=None: 结束时间  str
    """
    if startdate is None:
        startdate = "2000-01-01"
    if enddate is None:
        enddate = datetime.datetime.now().strftime("%Y-%m-%d")
    _startdate=datetime.datetime.strptime(startdate,"%Y-%m-%d")
    _enddate=datetime.datetime.strptime(enddate,"%Y-%m-%d")
    date_list=get_date_list(_startdate,_enddate)
    Q_list = []
    for D in date_list:
        if D.month in [1,2,3]:
            Q_str= "%s-1"%D.year

        elif D.month in [4,5,6]:
            Q_str= "%s-2"%D.year
        elif D.month in [7,8,9]:
            Q_str= "%s-3"%D.year
        elif D.month in [10,11,12]:
            Q_str= "%s-4"%D.year

        if  Q_str in Q_list:
            pass
        else:
            Q_list.append(Q_str)
    return Q_list
            
def gen_dates(b_date, days):
    """
    docstring here
        :param b_date: start date 
        :param days:  add days
    """
    
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield b_date + day*i


def get_date_list(start=None, end=None):
    """
    获取日期列表
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    if start is None:
        start = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
    if end is None:
        end = datetime.datetime.now()
    data = []
    for d in gen_dates(start, (end-start).days):
        data.append(d)
    return data
