#-*-coding=utf-8-*-
import requests 
from lxml import etree
import re
from pyecharts import Map,Line,Page,configure,Grid,Pie
import webbrowser
from datetime import date
import time
import numpy as np 

def get_html_text(url):
    headers =  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    req = requests.get(url,headers=headers)
    '''
    其中 req.encoding 根据响应头中的 charset 判断网站编码，如果没有设置则默认返回 iso-8859-1 编码，而req.apparent_encoding
    则通过网页内容来判断其编码。令req.encoding=req.apparent_encoding就不会出现乱码问题。
    '''
    req.raise_for_status()
    req.encoding=req.apparent_encoding
    return req.text,etree.HTML(req.text)


def get_date():
    today = date.today()
    return today

def creat_map(city_dict,date_):
    map_ = Map(f"至{date_}深圳市新型冠状病毒感染的肺炎确诊病例分布", width=1350, height=500)
    cities = []
    value = []
    for city in city_dict:
        cities.append(city)
        value.append(city_dict[city][0])
    value =  np.array(value)
    total = np.sum(value)
    rate = value/total
    map_.add( "", cities[:-1], value[:-1], maptype="深圳", is_visualmap=True, visual_text_color='#000')
    return map_,cities,rate

def creat_line(cities_dict,date_y):

    #num = [str(i) for i in range(1,n+1)]
    n = len(date_y[::2])
    all_nmber = np.array([0]*n)

    line= Line(f"前{n}次新型冠状病毒感染的肺炎确诊病例播报情况",width=1350, height=500)
    for key in cities_dict:
        number = cities_dict[key][::-2]
        number = np.array(number)
        #print(number)
        all_nmber += number
        line.add(f"{key}", date_y[::-2], number,is_label_show=True,yaxis_name="人数(个)",xaxis_name='播报顺序(次)',legend_top='5%')
    line.add('总人数',date_y[::-2],all_nmber,is_label_show=True,yaxis_name="人数(个)",xaxis_name='播报顺序(次)',legend_top='5%')
    print(f'深圳市总体型冠状病毒感染的肺炎确诊人数(最新):{all_nmber[-1]}人')
    return line

def create_pie(cities,rate):
    pie = Pie('各区确诊人数占比',width=1350, height=600)
    pie.add("",cities,rate,is_label_show=True,radius=[30, 75],rosetype="area",legend_top="5%")
    return pie

def split_channel():
    print('---------------------------------------------------------------------------------------------------------------------')
    print()
    print('---------------------------------------------------------------------------------------------------------------------')

if __name__ == '__main__':

    #爬取新型冠状性病毒肺炎新闻网址
    urls = []
    date_list = []
    base_url = 'http://wjw.sz.gov.cn/yqxx'
    for i in range(5):
        if i == 0:
            url = f'http://wjw.sz.gov.cn/yqxx/index.htm'
        else:
            url = f'http://wjw.sz.gov.cn/yqxx/index_{i}.htm'
        imfos,html = get_html_text(url)
        items = html.xpath('//div[@class="right_list"]//li')
        #print(imfos)
        #print(items)
        for item in items:
            #print(item.xpath('a/text()'))
            if '新冠肺炎疫情情况' in item.xpath('a/text()')[0] or '新型冠状病毒感染的肺炎疫情情况' in item.xpath('a/text()')[0]:

                urls.append(base_url + item.xpath('a/@href')[0].strip('.'))
                date_list.append(item.xpath('strong/text()')[0])

        # print(urls)
        # print(date_list)

    #获取新型冠状病毒性肺炎新闻内容人数统计
    city_dict = {'南山区': [], '福田区': [], '龙岗区': [], '宝安区': [], '龙华区': [],
    '罗湖区': [], '光明区': [], '坪山区': [], '盐田区': [], '大鹏新区': [], '其他（指由机场、车站、码头、关口、路卡等直接送往定点医院的)': []}
    for url in urls:
        imfos,html = get_html_text(url)
        items = html.xpath('//div[@class="TRS_Editor"]/p[@align="justify"]/text()')
        main_contents = items[2]
        pattern = re.compile(r'\d+')
        number = [int(i) for i in re.findall(pattern,main_contents)]
        index = 0
        for city in city_dict:
            city_dict[city].append(number[index]) 
            index += 1
        time.sleep(2)

    print(city_dict)

    #画图
    #constants.CITY_NAME_PINYIN_MAP['深圳市']='shenzhen'
    today = get_date()
    configure(global_theme='dark')
    grid = Grid()
    page = Page() 
    map_,cities,rate = creat_map(city_dict,today)
    line = creat_line(city_dict,date_list)
    pie = create_pie(cities,rate)
    page.add(map_)
    # grid.add(map_)
    # grid.add(line)
    page.add(line)
    page.add(pie)
    #grid.render()
    page.render()
    webbrowser.open(f'render.html')


