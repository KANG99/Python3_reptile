from urllib.parse import urlencode
import requests
import os
from hashlib import md5

'''
aid=24&app_name=web_search&offset=40&format=json&
keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&
en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1573573996274
'''
def create_url(offset=20):

	base_url ='https://www.toutiao.com/api/search/content/?'
	parmaters = {'aid':'24',
	'app_name':'web_search',
	'offset':offset,
	'format':'json',
	'keyword':'街拍',
	'autoload':'true',
	'count':'20',
	'en_qc':'1',
	'cur_tab':'1',
	'from':'search_tab',
	'pd':'synthesis',
	}
	url = base_url + urlencode(parmaters)
	return url


def get_page(offset):
	url = create_url(offset)
	headers = {
	        'cookie': 'tt_webid=6758447871114184196; s_v_web_id=b61a13dbe99133c73baac3a3145ed12a; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6758447871114184196; csrftoken=0ed9fd6e67fa3402353b28a7d94f8dcc; __tasessionId=xbq6h2k1o1573617156571',
	        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
	        'x-requested-with': 'XMLHttpRequest',
	        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
	    }
	try:
		reponse = requests.get(url,headers=headers)
		if reponse.status_code == 200:
			return reponse.json()
	except requests.ConnectionError as e:
		return None

def save_pictures(image_list):
	for image_url in image_list:
		try:
			req = requests.get(image_url['url'])
			if req.status_code == 200:
				content = req.content
				filename = '{}/{}.jpg'.format(title,md5(content).hexdigest())
				with open(filename,'wb') as f:
					f.write(content)
				print("save {} sussessfully!".format(filename))
		except requests.ConnectionError as e:
			print('error:',e)

if __name__ == '__main__':

	offset = 0
	json_data = get_page(offset)
	data_list = json_data.get('data')
	#print(data.get(title))
	#print(len(datas))
	for data in data_list:
		#if data.get('title'):
		title = data.get('title')
		if title:
			if not os.path.exists(title):
				os.mkdir(title)
				#print(title)
				image_list = data['image_list']
				save_pictures(image_list)

