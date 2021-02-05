# 使用request + BeautifulSoup提取12365auto投诉信息
import requests
from bs4 import BeautifulSoup
import pandas as pd


# 根据request_url得到soup
def get_page_content(request_url):
    # 得到页面的内容
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=10)
    content = html.text
    #print(content)

    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

# 分析当前页面的投诉
def analysis(soup):
    temp = soup.find('div',class_="tslb_b")
    # 创建DataFrame
    df = pd.DataFrame(columns = ['编号','品牌','车系', '车型', '问题简述', '问题描述', '投诉时间', '投诉状态'])
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        temp = {}
        td_list = tr.find_all('td')
        # 第一个tr没有td，其余都有8个td
        if len(td_list) > 0:
            # 解析各个字段的内容
            # 放到DataFrame中
            temp['编号'], temp['品牌'], temp['车系'], temp['车型'], temp['问题简述'], temp['问题描述'], temp['投诉时间'], temp['投诉状态'] = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            df = df.append(temp,ignore_index=True)
    return df

page_num = 20
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'

result = pd.DataFrame(columns = ['编号','品牌','车系', '车型', '问题简述', '问题描述', '投诉时间', '投诉状态'])
for i in range(page_num):
    request_url = base_url+str(i+1)+'.shtml'
    soup = get_page_content(request_url)
    df = analysis(soup)
    #print(df)
    result = result.append(df)
    
result.to_csv('D:/Homework', index=False)
