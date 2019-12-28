import requests
from pyquery import PyQuery as pq 
import json


url = 'https://www.zhihu.com/explore'
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
html = requests.get(url,headers=headers).text
# html = etree.HTML(html)
# html = etree.tostring(html).decode('utf-8')
#print(html)
doc = pq(html)
items = doc('.ExploreRoundtableCard-questionItem ').items()
l = []
Dict = {}
answers = ''
for item in items:
	question = item.find('.ExploreRoundtableCard-questionTitle').text()
	Dict['question'] = question
	info = item.find('.ExploreRoundtableCard-questionTitle').attr.href
	answer_url = 'https://www.zhihu.com'+info
	#print(anwser_url)
	html = requests.get(answer_url,headers=headers)
	doc = pq(html.text)
	answer_items = doc('.RichContent-inner').items()
	#print(anwser_items)
	for answer_item in answer_items:
		answers += answer_item.text()+'\n'
	Dict['answers'] = answers
	l.extend[Dict.copy()]
with open('zhihu.json','a',encoding='utf-8') as f:
	f.write(json.dumps(l))
with open('zhihu.json','r',encoding='utf-8') as f:
	s = f.read()
	s = json.loads(s)
	print(s)