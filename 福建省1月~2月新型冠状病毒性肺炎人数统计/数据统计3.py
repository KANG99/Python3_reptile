#-*-coding=utf-8-*-
import requests 
from lxml import etree
import re
from pyecharts import Map,Line,Page,configure
import webbrowser
from datetime import date
import time
import numpy as np 
import json


def get_html_text(url):
    headers =  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    req = requests.get(url,headers=headers)
    '''
    其中 req.encoding 根据响应头中的 charset 判断网站编码，如果没有设置则默认返回 iso-8859-1 编码，而req.apparent_encoding
    则通过网页内容来判断其编码。令req.encoding=req.apparent_encoding就不会出现乱码问题。
    '''
    req.raise_for_status()
    req.encoding=req.apparent_encoding
    return req.text

def parse_html_text(item):
    html2 = etree.HTML(data2)
    imfos = html2.xpath('//div[@class="TRS_Editor"]/p/font[@style="font-size: 14pt"]/text()')
    return imfos

def get_valid_imfos(imfos):
   
    valid_imfos = ''.join([v for v in ''.join(imfos) if v != ' ' and v !='\n' and v !='\xa0' and v !='\u3000']).split('。')
    return valid_imfos

def get_attr_value(valid_imfos):
    #print(valid_imfos)
    imfos_list = valid_imfos.split('；')
    attr = []
    value = []
    for i in imfos_list:
        #print(i)
        city_name = i[:3]
        pattern = re.compile(r'\d+')
        number = re.findall(pattern,i)[0]
        #print(number) 
        #print(city_name,number)
        attr.append(city_name)
        value.append(number)
    value  = [int(x) for x in value]
    #print(attr,value)
    return attr,value

def make_cities_dict(n):
    cities = ['福州市', '厦门市', '漳州市', '泉州市', '三明市', '莆田市', '南平市', '龙岩市', '宁德市']
    cities_dict = {}
    for city in cities:
        cities_dict[city] = [0]*n
    for i in range(n):
        for key in city_list[i]:
            if key in cities_dict:
                cities_dict[key][i] = city_list[i][key]
    return cities_dict

def get_date():
    today = date.today()
    return today

def creat_map(value,date_):
    cities = ['福州市', '厦门市', '漳州市', '泉州市', '三明市', '莆田市', '南平市', '龙岩市', '宁德市'] 
    map = Map(f"至{date_}福建新型冠状病毒感染的肺炎确诊病例分布", width=1600, height=500)
    map.add( "", cities, value, maptype="福建", is_visualmap=True, visual_text_color='#000')
    return map

def creat_line(cities_dict,date_,date_y,n=5):
    all_nmber = np.array([0]*n)
    line = Line(f"前{n}次新型冠状病毒感染的肺炎确诊病例播报情况",width=1600, height=500)
    for key in cities_dict:
        number = cities_dict[f'{key}'][::-1]
        number = [int(x) for x in number]
        number = np.array(number)
        all_nmber += number
        line.add(f"{key}", date_y[::-1], number,is_label_show=True,line_width=2,yaxis_name="人数(个)",xaxis_name='播报时间(天)')
    line.add('总人数',date_y[::-1],all_nmber,is_label_show=True,line_width=2,yaxis_name="人数(个)",xaxis_name='播报时间(天)')
    print(f'福建总体型冠状病毒感染的肺炎确诊人数(最新):{all_nmber[-1]}人')
    return line



if __name__ == '__main__':

    #爬取新型冠状性病毒肺炎新闻网址
    urls = []
    date_list = []
    for i in range(1,10):
        url = f'http://wjw.fujian.gov.cn/was5/web/search?sortfield=-docreltime&templet=docs.jsp&channelid=285300&classsql=chnlid%3D1698&page={i}'
        imfos = get_html_text(url)
        imfos = ''.join([imfo.strip('\r\n').strip('<br>') for imfo in imfos.strip() if imfo != '' and imfos !='\r\n'])
        #imfos = imfos.split(' ')
        imfos = eval(imfos)
        #print(type(imfos['docs']))
        valid_imfos = imfos['docs']
        for imfo in valid_imfos:
            #print(imfo)
            if '新型冠状病毒肺炎疫情情况' in imfo['title'] or '新型冠状病毒感染的肺炎疫情情况' in imfo['title']:
                urls.append(imfo['chnldocul'])
                date_list.append(imfo['time'])
        time.sleep(2)
    # print(urls)
    # urls = ['http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200210_5192203.htm', 'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200209_5192015.htm',
    #  'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200208_5191780.htm', 'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200207_5191350.htm',
    #   'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200206_5190664.htm', 'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200205_5190031.htm', 
    #   'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200204_5188911.htm', 'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200203_5188217.htm', 
    #   'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200202_5187726.htm','http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200201_5187438.htm', 
    #   'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202001/t20200131_5187175.htm']


    #爬取新型冠状病毒性肺炎新闻内容数据
    city_list = []
    date_y = []
    date_index = 0

    for url in urls:
        data2 = get_html_text(url)
        imfos = parse_html_text(data2)
        valid_imfos = get_valid_imfos(imfos)
        index = 2
        #print(valid_imfos)
        url_date = date_list[date_index]
        date_index += 1
        if len(valid_imfos)>2:
            attr,value = get_attr_value(valid_imfos[index])
            n = 0
            city_dict = {}
            for city in attr:
                city_dict[city] = value[n]
                n += 1
            city_list.append(city_dict.copy())
            date_y.append(url_date)
            time.sleep(2)

    #画图
    configure(global_theme='dark')
    times = len(city_list)
    cities_dict = make_cities_dict(times)
    today = get_date()
    print(cities_dict)
    all_num = []
    for key in cities_dict:
        all_num.append(cities_dict[f'{key}'][0])
    line = creat_line(cities_dict,today,date_y,times)
    #print(all_num)
    page = Page()  
    map_ = creat_map(all_num,today)
    page.add(map_)
    page.add(line)
    page.render()
    webbrowser.open(f'render.html')


