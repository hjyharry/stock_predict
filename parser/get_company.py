import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import pymysql

def trim(s):
    r = re.findall('[\S]+', s)
    return " ".join(r)

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


def parse_company_detail(stock_id):
    url = "http://quotes.money.163.com/f10/gszl_{stock_id}.html#01f02".format(stock_id=stock_id)
    response = requests.get(url)
    html = response.content.decode('utf-8')
    parser = BeautifulSoup(html)
    label_detail_list = []
    company_info = {}
    try:
        labels_detail = parser.find_all('td', class_="td_width160")
        labels_detail_2 = parser.find_all('td', colspan="3")
        labels_detail_3 = parser.find('div', class_="col_r_01").find('table',class_="table_bg001 border_box limit_sale table_details").find_all('td', class_="")
    except:
        company_info['code'] = stock_id
        company_info['form'] = None
        company_info['region'] = None
        company_info['name_c'] = None
        company_info['location'] = None
        company_info['full_name'] = None
        company_info['phone_c'] = None
        company_info['name_e'] = None
        company_info['email_c'] = None
        company_info['capital'] = None
        company_info['chairman'] = None
        company_info['number'] = None
        company_info['secretary'] = None
        company_info['representative'] = None
        company_info['phone_s'] = None
        company_info['general_manager'] = None
        company_info['fax_s'] = None
        company_info['website'] = None
        company_info['newspaper'] = None
        company_info['business_m'] = None
        company_info['business_s'] = None
        company_info['history'] = None
        company_info['date_set'] = None
        company_info['date_launch'] = None
        company_info['type'] = None
        company_info['value'] = None
        company_info['num_issue'] = None
        company_info['price_issue'] = None
        company_info['total_price'] = None
        company_info['total_issue'] = None
        company_info['rate_issue'] = None
        company_info['PE_ratio'] = None
        company_info['earn_per'] = None
        company_info['net_worth'] = None
        company_info['open_first'] = None
        company_info['close_first'] = None
        company_info['turnover_first'] = None
        company_info['underwriter'] = None
        company_info['sponsor_list'] = None
        company_info['firm_account'] = None
        return company_info

    for label_detail in labels_detail:
        label_detail_list.append(label_detail.get_text())
    for label_detail_2 in labels_detail_2:
        label_detail_list.append(trim(label_detail_2.get_text()))
    for label_detail_3 in labels_detail_3:
        label_detail_list.append(trim(label_detail_3.get_text().strip()))

    company_info['code'] = stock_id
    company_info['form'] = label_detail_list[0]
    company_info['region'] = label_detail_list[1]
    company_info['name_c'] = label_detail_list[2]
    company_info['location'] = label_detail_list[3]
    company_info['full_name'] = label_detail_list[4]
    company_info['phone_c'] = label_detail_list[5]
    company_info['name_e'] = label_detail_list[6]
    company_info['email_c'] = label_detail_list[7]
    company_info['capital'] = label_detail_list[8]
    company_info['chairman'] = label_detail_list[9]
    company_info['number'] = label_detail_list[10]
    company_info['secretary'] = label_detail_list[11]
    company_info['representative'] = label_detail_list[12]
    company_info['phone_s'] = label_detail_list[13]
    company_info['general_manager'] = label_detail_list[14]
    company_info['fax_s'] = label_detail_list[15]
    company_info['website'] = label_detail_list[16]
    company_info['newspaper'] = label_detail_list[17]
    company_info['business_m'] = label_detail_list[18]
    company_info['business_s'] = label_detail_list[19]
    company_info['history'] = label_detail_list[20]
    company_info['date_set'] = label_detail_list[21]
    company_info['date_launch'] = label_detail_list[22]
    company_info['type'] = label_detail_list[23]
    company_info['value'] = label_detail_list[24]
    company_info['num_issue'] = label_detail_list[25]
    company_info['price_issue'] = label_detail_list[26]
    company_info['total_price'] = label_detail_list[27]
    company_info['total_issue'] = label_detail_list[28]
    company_info['rate_issue'] = label_detail_list[29]
    company_info['PE_ratio'] = label_detail_list[30]
    company_info['earn_per'] = label_detail_list[31]
    company_info['net_worth'] = label_detail_list[32]
    company_info['open_first'] = label_detail_list[33]
    company_info['close_first'] = label_detail_list[34]
    company_info['turnover_first'] = label_detail_list[35]
    company_info['underwriter'] = label_detail_list[36]
    company_info['sponsor_list'] = label_detail_list[37]
    company_info['firm_account'] = label_detail_list[38]

    return company_info

def main():
    company_list = []
    code_list = get_code()
    for i in range(len(code_list)):
        company = parse_company_detail(code_list[i])
        company_list.append(company)
        print(code_list[i] + "爬取完成")

    pd.DataFrame(company_list).to_sql(name='stock_company_info',
                                      con='mysql+pymysql://root:hjyharry981221@localhost:3306/stock?charset=utf8',
                                      if_exists='append', index=False)

if __name__ == "__main__":
    main()