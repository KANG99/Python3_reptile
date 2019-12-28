import requests
import re
import json
import time

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
	
	pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
	items = re.findall(pattern,html)
	if items:
		for item in items:
			#print(item)
			yield{'index':item[0],'image':re.sub('@.*?$','',item[1]),'title':item[2].strip(),'actor':item[3].strip()[3:] if len(item[3])>3 else '','time':item[4].strip()[5:] if len(item[4])>5 else '','score':item[5].strip()+item[6].strip()}

if __name__ == '__main__':

	
	for i in range(0,100,10):
		url = 'http://maoyan.com/board/4?offset='+str(i)
		html,status_code = get_one_page(url)
		#print(html)
		#print(status_code)
		if status_code == 200:
			for item in parse_page(html):
				#print(item)
				with open('result.txt','a',encoding='utf-8') as f:
					content = json.dumps(item)+'\n'
					f.write(content)
			time.sleep(1)
			print('top:'+str(i+10))
		else:
			print(status_code)
	'''			
	with open('result.txt','rb') as f:
		content = f.readlines()
		if content:
			for s in content:
				s = json.loads(s)
				print(s)
	'''