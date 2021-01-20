import datetime
import json
import random
import pymysql
import pandas as pd
import requests
from bs4 import BeautifulSoup

#获取股票类型id与类型名称
def get_catgory_id():
    url = "http://quotes.money.163.com/old/#query=hy001000&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0"

    response = requests.get(url)
    html = response.content.decode('utf-8')
    parser = BeautifulSoup(html, 'lxml')

    stock_catlogs = parser.find('li', id="f0-f6").find('ul', class_="hidden").find_all('li')

    cate_list = []
    for catlog_list in stock_catlogs:
        cate_list.append({'cate_id':catlog_list['qid'],'cate_name':catlog_list.a['title']})

    pd.DataFrame(cate_list).to_sql(name='stock_category',
                                          con='mysql+pymysql://root:hjyharry981221@localhost:3306/stock?charset=utf8',
                                          if_exists='append', index=False)

    print("股票类型信息爬取完成")

if __name__ == "__main__":
    get_catgory_id()