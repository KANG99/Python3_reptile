import requests
from pyquery import PyQuery as pq 



url = 'https://www.zhihu.com/explore'
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
html = requests.get(url,headers=headers).text
# html = etree.HTML(html)
# html = etree.tostring(html).decode('utf-8')
#print(html)
doc = pq(html)
items = doc('.ExploreRoundtableCard-questionItem ').items()
for item in items:
	with open('zhihu.txt','a',encoding='utf-8') as f:
			f.write('\n'+'='*50+'\n')
	question = item.find('.ExploreRoundtableCard-questionTitle').text()
	with open('zhihu.txt','a',encoding='utf-8') as f:
			f.write(question+'\n')
	info = item.find('.ExploreRoundtableCard-questionTitle').attr.href
	anwser_url = 'https://www.zhihu.com'+info
	#print(anwser_url)
	html = requests.get(anwser_url,headers=headers)
	doc = pq(html.text)
	anwser_items = doc('.RichContent-inner').items()
	#print(anwser_items)
	for anwser_item in anwser_items:
		with open('zhihu.txt','a',encoding='utf-8') as f:
			f.write(anwser_item.text()+'\n')