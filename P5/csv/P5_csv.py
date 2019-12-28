import requests
from pyquery import PyQuery as pq 
import csv


url = 'https://www.zhihu.com/explore'
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
html = requests.get(url,headers=headers).text
# html = etree.HTML(html)
# html = etree.tostring(html).decode('utf-8')
#print(html)
Dict = {}
fieldnames = ['question','answers']
doc = pq(html)
l = []

items = doc('.ExploreRoundtableCard-questionItem ').items()
for item in items:
	question = item.find('.ExploreRoundtableCard-questionTitle').text()
	Dict['question'] = question
	info = item.find('.ExploreRoundtableCard-questionTitle').attr.href
	anwser_url = 'https://www.zhihu.com'+info
	#print(anwser_url)
	html = requests.get(anwser_url,headers=headers)
	doc = pq(html.text)
	anwser_items = doc('.RichContent-inner').items()
	#print(anwser_items)
	n = 1
	Dict['answers'] = ''
	for anwser_item in anwser_items:
		Dict['answers'] += anwser_item.text()
		l.append(Dict.copy())

with open('zhihu.csv','a',encoding='utf-8') as csvfile:
		writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
		for i in l:
			writer.writerow(i)
			