from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from django.http import Http404,HttpResponse
from stock.models import *
from login.models import User

import datetime
import json
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup

def refresh(request):
    cur_stock = CUR_STOCK.objects.values()
    cur_stock = list(cur_stock)

    stock_categorys = category.objects.values()
    stock_categorys = list(stock_categorys)

    if request.method == "POST" and 'refresh_btn'in request.POST:
        CUR_STOCK.objects.all().delete()
        main()
        return redirect('/index/')
    elif request.method == "POST" and 'selected_category' in request.POST:
        cate_id = request.POST.get("selected_category")

        current_cate_id = cate_id
        cur_stock = CUR_STOCK.objects.filter(CODE__category_id = cate_id).values()
        cur_stock = list(cur_stock)

        return render(request,'stock/index.html',{"cur_stocks":cur_stock,"stock_categorys":stock_categorys,"current_id":current_cate_id})

    return render(request, 'stock/index.html', {"cur_stocks":cur_stock,"stock_categorys":stock_categorys})

def stock_detail(request):
    next_url = request.path_info
    id = next_url[7:]
    option_year = []

    detail = company_info.objects.filter(code__code = id).get()
    cur_stock = CUR_STOCK.objects.filter(CODE__code = id).get()

    stock_history = history_data.objects.filter(code = id).values()
    stock_history = list(stock_history)

    #返回目标股票的年份信息
    for i in range(len(stock_history)):
        stock_history[i]['date'] = stock_history[i]['date'].strftime('%Y-%m-%d')
        year = stock_history[i]['date'][:4]
        if year not in option_year:
            option_year.append(year)

    #获取K线图所需数据
    k_stock = history_data.objects.filter(code = id).values('date','open','close','low','high','volumn').order_by('date')
    k_stock = list(k_stock)
    for i in range(len(k_stock)):
        k_stock[i]['date'] = k_stock[i]['date'].strftime('%Y/%m/%d')
    k_list = []
    for i in range(len(k_stock)):
        k_list.append(list(k_stock[i].values()))


    if request.method == "POST" and 'selected_s' in request.POST:
        year = request.POST.get('selected_year')
        year = int(year)

        #获取股票季度值
        season = request.POST.get('selected_season')
        if season == "season1":
            start_date = datetime.date(year, 1, 1)
            end_date = datetime.date(year, 3, 31)
            current_season = "season1"
        elif season == "season2":
            start_date = datetime.date(year, 4, 1)
            end_date = datetime.date(year, 6, 30)
            current_season = "season2"
        elif season == "season3":
            start_date = datetime.date(year, 7, 1)
            end_date = datetime.date(year, 9, 30)
            current_season = "season3"
        elif season == "season4":
            start_date = datetime.date(year, 10, 1)
            end_date = datetime.date(year, 12, 31)
            current_season = "season4"
        else:
            start_date = datetime.date(year, 1, 1)
            end_date = datetime.date(year, 12, 31)
            current_season = "all"

        selected_stock = history_data.objects.filter(code=id,date__range=(start_date,end_date)).values()
        selected_stock = list(selected_stock)

        for i in range(len(selected_stock)):
            selected_stock[i]['date'] = selected_stock[i]['date'].strftime('%Y-%m-%d')
            year = selected_stock[i]['date'][:4]
            if year not in option_year:
                option_year.append(year)

        return render(request,'stock/detail.html',{"company_detail":detail,"cur_stock":cur_stock,"selected_stock":selected_stock,"current_year":year,"current_season":current_season,"option_year":option_year,"k_data":k_list})
    elif request.method == "POST" and 'selected_k' in request.POST:
        year = request.POST.get('selected_year')
        current_year = year

        start_date = datetime.date(int(current_year),1,1)
        end_date = datetime.date(int(current_year),12,31)

        k_stock = history_data.objects.filter(code=id,date__range=(start_date,end_date)).values('date', 'open', 'close', 'low', 'high', 'volumn').order_by('date')
        k_stock = list(k_stock)
        for i in range(len(k_stock)):
            k_stock[i]['date'] = k_stock[i]['date'].strftime('%Y/%m/%d')
        k_list = []
        for i in range(len(k_stock)):
            k_list.append(list(k_stock[i].values()))

        return render(request,'stock/detail.html',{"company_detail":detail,"cur_stock":cur_stock,"stock_history":stock_history,"current_year_k":current_year,"option_year":option_year,"k_data":k_list})
    elif request.method == "POST" and "favourite" in request.POST:
        user_id = request.session.get("user_id")
        code = id
        if not myFavourite.objects.filter(id=user_id,code=code):
            Favourite = {
                "id":User.objects.filter(id=user_id)[0],
                "code": stock_relate.objects.filter(code = code)[0]
            }
            myFavourite.objects.create(**Favourite)
        return redirect('/index/' + code)


    return render(request,'stock/detail.html',{"company_detail":detail,"cur_stock":cur_stock,"stock_history":stock_history,"option_year":option_year,"k_data":k_list})

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


def get_catgory_id():
    url = "http://quotes.money.163.com/old/#query=hy001000&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0"

    response = requests.get(url, headers)
    html = response.content.decode('utf-8')
    parser = BeautifulSoup(html, 'html')

    stock_catlogs = parser.find('li', id="f0-f6").find('ul', class_="hidden").find_all('li')

    cate_list = []
    for catlog_list in stock_catlogs:
        cate_list.append({'cate_id':catlog_list['qid'],'cate_name':catlog_list.a['title']})

    return cate_list

def get_cur_detail(category_id):
    url = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=PLATE_IDS%3A{category_id}&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=9999&type=query".format(
        category_id=category_id)

    req = requests.get(url, headers)
    str_data = req.content
    json_info = json.loads(str_data)
    stock_info = json_info['list']

    for i in range(len(stock_info)):
        stock_info[i]['DATE'] = str(datetime.datetime.now().replace(microsecond=0))
        if stock_info[i].__contains__('MFRATIO'):
            stock_info[i]['MFRATIO_1'] = stock_info[i]['MFRATIO']['MFRATIO2']
            stock_info[i]['MFRATIO_2'] = stock_info[i]['MFRATIO']['MFRATIO10']
            del stock_info[i]['MFRATIO']
        else:
            stock_info[i]['MFRATIO_1'] = 0
            stock_info[i]['MFRATIO_2'] = 0

        if not stock_info[i]['MFRATIO_1']:
            stock_info[i]['MFRATIO_1'] = 0
        if not stock_info[i]['MFRATIO_2']:
            stock_info[i]['MFRATIO_2'] = 0

        if stock_info[i].__contains__('SNAME'):
            del stock_info[i]['SNAME']
        if stock_info[i].__contains__('SYMBOL'):
            del stock_info[i]['SYMBOL']
        if stock_info[i].__contains__('CODE'):
            stock_info[i]['CODE'] = stock_info[i]['CODE'][1:]
        if stock_info[i].__contains__('ANNOUNMT'):
            del stock_info[i]['ANNOUNMT']

        if not stock_info[i].__contains__('FIVE_MINUTE'):
            stock_info[i]['FIVE_MINUTE'] = 0
        if not stock_info[i].__contains__('HS'):
            stock_info[i]['HS'] = 0
        if not stock_info[i].__contains__('LB'):
            stock_info[i]['LB'] = 0
        if not stock_info[i].__contains__('WB'):
            stock_info[i]['WB'] = 0
        if not stock_info[i].__contains__('ZF'):
            stock_info[i]['ZF'] = 0
        if not stock_info[i].__contains__('PE'):
            stock_info[i]['PE'] = 0
        if not stock_info[i].__contains__('MCAP'):
            stock_info[i]['MCAP'] = 0
        if not stock_info[i].__contains__('TCAP'):
            stock_info[i]['TCAP'] = 0
        if not stock_info[i].__contains__('MFSUM'):
            stock_info[i]['MFSUM'] = 0

    stock_DF = pd.DataFrame(stock_info)

    stock_DF = stock_DF[['CODE','NAME','PRICE','PERCENT','UPDOWN','FIVE_MINUTE','OPEN','YESTCLOSE','HIGH','LOW','VOLUME','TURNOVER','HS','LB','WB','ZF','PE','MCAP','TCAP','MFSUM','MFRATIO_1','MFRATIO_2','DATE']]
    return stock_DF

def main():
    cur_detail_list = []
    for i in range(len(get_catgory_id())):
        cur_detail_list.append(get_cur_detail(get_catgory_id()[i]['cate_id']))
        cur_detail_df = pd.concat(cur_detail_list,ignore_index=True)

    cur_detail_df.to_sql(name='cur_stock',con='mysql+pymysql://root:hjyharry981221@localhost:3306/stock?charset=utf8',if_exists='append',index=False)
