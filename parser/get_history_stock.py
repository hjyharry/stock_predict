import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql

content_list = []

def get_code():
    db = pymysql.connect("localhost", "root", "hjyharry981221", "stock")
    cursor = db.cursor()
    sql = """select code from stock_relate order by code asc"""
    cursor.execute(sql)
    code_list = []
    result = cursor.fetchall()
    for row in result:
        code = row[0]
        code_list.append(code)

    return code_list

def get_start_year(code):
    url = "http://quotes.money.163.com/trade/lsjysj_{}.html#01b07".format(code)
    try:
        response = requests.get(url=url)
        html = response.content.decode('utf-8')
        parser = BeautifulSoup(html, 'lxml')
        year = parser.find('div',class_="bd").find('input',{"name":"date_start_value"})['value']
        return year
    except:
        pass


def get_stock_history(code):
    if code[:1] in ["0", "1", "2", "3"]:
        url = "http://quotes.money.163.com/service/chddata.html?code=1{code}&start={start}&end=20210107&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(
            code=code, start=get_start_year(code))
    else:
        url = "http://quotes.money.163.com/service/chddata.html?code=0{code}&start={start}&end=20210107&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(
            code=code, start=get_start_year(code))

    try:
        response = requests.get(url=url).content
        html = BeautifulSoup(response, 'lxml')
        list = html.find('p').text.split('\r\n')
        list.remove(list[-1])

        for i in range(1, len(list)):
            content = list[i].split(",")
            content_list.append(content)

        df = pd.DataFrame(content_list)
        df.columns = (
        'date', 'code', 'name', 'close', 'high', 'low', 'open', 'yest_close', 'updown', 'percent', 'hs', 'volumn',
        'turnover', 'tcap', 'mcap')

        df.replace('None', '0', inplace=True)

        df['date'] = pd.to_datetime(df['date'])
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['open'] = df['open'].astype(float)
        df['yest_close'] = df['yest_close'].astype(float)
        df['updown'] = df['updown'].astype(float)
        df['percent'] = df['percent'].astype(float)
        df['hs'] = df['hs'].astype(float)
        df['volumn'] = df['volumn'].astype(float)
        df['turnover'] = df['turnover'].astype(float)
        df['tcap'] = df['tcap'].astype(float)
        df['mcap'] = df['mcap'].astype(float)
        df['code'].replace("'{}".format(code), "{}".format(code), inplace=True)

        del df['name']

        content_list.clear()
        print(code + "爬取成功")
        df.to_sql(name='stock_history_data',
                  con='mysql+pymysql://root:hjyharry981221@localhost:3306/stock?charset=utf8',
                  if_exists='append', index=False)

    except:
        print(code + "不存在或没有历史数据")
        pass


if __name__ == '__main__':
    code = get_code()
    for i in range(len(code)):
        get_stock_history(code[i])