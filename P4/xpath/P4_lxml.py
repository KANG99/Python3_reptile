import requests
import re
import json
import time
from lxml import etree


def get_one_page(url):

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text,response.status_code
        return None,response.status_code
    except requests.RequestException:
        return None

def parse_page(html):

    html = etree.HTML(html)

    img = [re.sub('@.*?$','',i) for i in html.xpath('//img/@data-src')]
    names = html.xpath('//p[@class="name"]/a/text()')
    stars =[i.strip()[3:] for i in html.xpath('//p[@class="star"]/text()')] 
    time = [i[5:] for i in html.xpath('//p[@class="releasetime"]/text()')]
    return img,names,stars,time



if __name__ == '__main__':

    imfos = {}

    for i in range(0,10,10):
        url = 'http://maoyan.com/board/4?offset='+str(i)
        html,status_code = get_one_page(url)
        #print(html)
        imfo = parse_page(html)
        imfos['TOP'+str(i+10)] = imfo
    print(imfos)
        #print(status_code)
        # for item in parse_page(html):
        #     #print(item)
        #     with open('result.txt','a',encoding='utf-8') as f:
        #         content = json.dumps(item)+'\n'
        #         f.write(content)
        # time.sleep(1)
        # print('top:'+str(i+10))
    '''         
    with open('result.txt','rb') as f:
        content = f.readlines()
        if content:
            for s in content:
                s = json.loads(s)
                print(s)
    '''