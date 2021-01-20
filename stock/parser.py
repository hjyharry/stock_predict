import re
from bs4 import BeautifulSoup
import requests
import random
import json
import pandas as pd
import pymysql

USER_AGENTS = [
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
        ]
Cookie = "_ntes_nnid=1ee52485629ec8171957281ae73675b9,1594993528051; _ntes_nuid=1ee52485629ec8171957281ae73675b9; mail_psc_fingerprint=2a2cd2b2b652aebc84ba8497e68505e3; nts_mail_user=undefined:-1:0; UM_distinctid=1754a3d17ac6b6-04197ce2d4b7ec-c781f38-1fa400-1754a3d17ad756; vjuids=8cfa1ad0.17573618cfc.0.ca57f65c387e; BAIDU_SSP_lcr=https://cn.bing.com/; _antanalysis_s_id=1606029909027; _ga=GA1.2.37195235.1606029956; _gid=GA1.2.1811344286.1606029956; ne_analysis_trace_id=1606029983177; vjlast=1603958574.1606030030.11; _ntes_stock_recent_plate_=hy009000%3A%E4%BF%A1%E6%81%AF%E6%8A%80%E6%9C%AF%7Chy013000%3A%E7%A7%91%E7%A0%94%E6%8A%80%E6%9C%AF; _ntes_stock_recent_=1300002%7C0688229%7C1300343%7C1002174%7C1000676%7C1300333%7C0601857%7C0600867; _ntes_stock_recent_=1300002%7C0688229%7C1300343%7C1002174%7C1000676%7C1300333%7C0601857%7C0600867; _ntes_stock_recent_=1300002%7C0688229%7C1300343%7C1002174%7C1000676%7C1300333%7C0601857%7C0600867; pgr_n_f_l_n3=2c5bd5169e86fed616060320739359583; vinfo_n_f_l_n3=2c5bd5169e86fed6.1.10.1603268318021.1605778207964.1606032078921"
headers = {
    'User-agent': random.choice(USER_AGENTS), #设置get请求的User-Agent，用于伪装浏览器UA
    'Cookie': Cookie,
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8',
    'Host': 'http://quotes.money.163.com',
    'Referer': 'http://quotes.money.163.com/old/'
}


def get_code():
    db = pymysql.connect("localhost", "root", "hjyharry981221", "stock")
    cursor = db.cursor()
    sql = """select code from stock_cur_stock order by code asc"""
    cursor.execute(sql)
    code_list = []
    result = cursor.fetchall()
    for row in result:
        code = row[0]
        code_list.append(code)

    return code_list


def get_history_detail(stock_id, year, season):
    url = "http://quotes.money.163.com/trade/lsjysj_{stock_id}.html?year={year}&season={season}".format(
        stock_id=stock_id, year=year, season=season)

    response = requests.get(url, headers)
    html = response.content.decode('utf-8')
    parser = BeautifulSoup(html, 'lxml')

    stock_dict = {}
    stock_dict_list = []

    try:
        # 爬取表中数据
        tdetails = parser.find('table', class_="table_bg001 border_box limit_sale").find_all('td')
        # 将表头信息放入列表stock_keys中

        # 将表中数据放入列表stock_detail中
        stock_detail = []
        for td in tdetails:
            stock_detail.append(td.string)

        # 将stock_detail中数据按照
        stock_detail_list = []
        for i in range(0, len(stock_detail), 11):
            stock_detail_list.append(stock_detail[i:i + 11])

        # 判断爬取数据是否存在，若不存在则给予None值

        for i in range(len(stock_detail_list)):
            stock_dict['date'] = stock_detail_list[i][0]
            stock_dict['open'] = stock_detail_list[i][1]
            stock_dict['high'] = stock_detail_list[i][2]
            stock_dict['low'] = stock_detail_list[i][3]
            stock_dict['close'] = stock_detail_list[i][4]
            stock_dict['updown'] = stock_detail_list[i][5]
            stock_dict['percent'] = stock_detail_list[i][6]
            stock_dict['volumn'] = stock_detail_list[i][7]
            stock_dict['turnover'] = stock_detail_list[i][8]
            stock_dict['zf'] = stock_detail_list[i][9]
            stock_dict['hs'] = stock_detail_list[i][10]
            stock_dict['code'] = stock_id
            stock_dict_list.append(stock_dict.copy())
        return stock_dict_list
    except:
        return stock_dict_list


def main():
    code_list = get_code()
    history = []

    for i in range(len(code_list)):
        for year in range(2005, 2021):
            history.extend(get_history_detail(code_list[i], year, 1))
            history.extend(get_history_detail(code_list[i], year, 2))
            history.extend(get_history_detail(code_list[i], year, 3))
            history.extend(get_history_detail(code_list[i], year, 4))
        df = pd.DataFrame(history)
        if df.empty:
            df.to_sql(name='stock_history_data',
                      con='mysql+pymysql://root:hjyharry981221@localhost:3306/stock?charset=utf8', if_exists='append',
                      index=False)
        else:
            df['open'] = df['open'].str.replace(',', '').astype(float)
            df['close'] = df['close'].str.replace(',', '').astype(float)
            df['high'] = df['high'].str.replace(',', '').astype(float)
            df['low'] = df['low'].str.replace(',', '').astype(float)
            df['updown'] = df['updown'].str.replace(',', '').astype(float)
            df['percent'] = df['percent'].str.replace(',', '').astype(float)
            df['volumn'] = df['volumn'].str.replace(',', '').astype(float)
            df['turnover'] = df['turnover'].str.replace(',', '').astype(float)
            df['zf'] = df['zf'].str.replace(',', '').astype(float)
            df['hs'] = df['hs'].str.replace(',', '').astype(float)
            df.to_sql(name='stock_history_data',
                      con='mysql+pymysql://root:hjyharry981221@localhost:3306/stock?charset=utf8', if_exists='append',
                      index=False)

        print(code_list[i] + "完成")
        history.clear()

if __name__ == "__main__":
    main()