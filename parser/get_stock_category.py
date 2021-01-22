import random
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from stock.models import stock_relate

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
    'User-agent': random.choice(USER_AGENTS),  # 设置get请求的User-Agent，用于伪装浏览器UA
    'Cookie': Cookie,
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8',
    'Host': 'http://quotes.money.163.com',
    'Referer': 'http://quotes.money.163.com/old/'
}


def get_catgory_id():
    url = "http://quotes.money.163.com/old/#query=hy001000&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0"

    response = requests.get(url, headers)
    html = response.content.decode('utf-8')
    parser = BeautifulSoup(html, 'html')

    stock_catlogs = parser.find('li', id="f0-f6").find('ul', class_="hidden").find_all('li')

    cate_list = []
    for catlog_list in stock_catlogs:
        cate_list.append({'cate_id': catlog_list['qid'], 'cate_name': catlog_list.a['title']})

    return cate_list


def parse_stock_category(category_id):
    url = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=PLATE_IDS%3A{category_id}&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=9999&type=query".format(
        category_id=category_id)

    req = requests.get(url, headers)
    str_data = req.content
    json_info = json.loads(str_data)
    stock_info = json_info['list']

    for i in range(len(stock_info)):
        stock_info[i]['category_id'] = category_id
        stock_info[i]['CODE'] = stock_info[i]['CODE'][1:]

    df = pd.DataFrame(stock_info)

    df.rename(columns={'CODE': 'code'}, inplace=True)
    df = df[['code', 'category_id']]
    return df

if __name__ == '__main__':
    stock_category_list = []
    db_code = []

    cate_list = get_catgory_id()

    db_sr = list(stock_relate.objects.values())
    for i in range(len(db_sr)):
        db_code.append(db_sr[i]['code'])

    for i in range(len(cate_list)):
        detail = parse_stock_category(cate_list[i]['cate_id'])
        stock_category_list.append(detail)
        stock_category_df = pd.concat(stock_category_list,ignore_index=True)

    stock_category_df.to_sql(name='stock_relate',con='mysql+pymysql://root:hjyharry981221@localhost:3306/stock?charset=utf8',if_exists='append',index=False)