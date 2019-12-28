import requests
from lxml import etree
import time
#import jieba
from wordcloud import WordCloud,ImageColorGenerator
from imageio import imread
import matplotlib.pyplot as plt
from PIL import Image
'''
本次任务请求豆瓣top250音乐网址，利用xpath提取出音乐简介后进行再过滤提取出歌星名字
再利用WordCloud生成词云图
查找Ubuntu下中文字体文件：fc-list :lang=zh
安装tkiner sudo apt install python-tk
'''

def get_result(url):

	headers = {'User-Agent':'Mozilla/63.0,Chrome/70.0.3538.77'}
	response = requests.get(url,headers=headers)
	html = etree.HTML(response.text)
	count = html.xpath('//tr[@class="item"]')
	title = [1]
	stars = list()
	for item in count:
		temp = item.xpath('normalize-space(td[2]/div/a/text())')#使用normalize去除换行符，但是会导致信息不全
		title = temp
		score = item.xpath('td[2]/div/div/span[2]/text()')
		blurb = item.xpath('td[2]/div/p/text()')
		st = blurb[0]
		star = st.split('/')[0]#通过/截取第一部分获取歌星名字
		#print(star)
		result = {'title':title,'star':star,'score':score,'blurb':blurb}
		print(result)
		stars.append(star)
	return stars

'''
def process_text(text):
	seg_generator = jieba.cut(text)
	seg_list = [i for i in seg_generator if i !=' ']
	seg_list=' '.join(seg_list)
	return seg_list
'''

def create_wordcloud(all_star,image_name):
	bg = imread(image_name)
	wc = WordCloud(font_path='ukai.ttc',background_color='white',
					max_words=2000,mask=bg,random_state=42)
	stars = ''
	for star in all_star:
		star = ''.join(star.split())
		star += ' '
		stars += star
	#print(stars)
	wc.generate(stars)
	image_colors = ImageColorGenerator(bg)
	wc.to_file('result.png')
	print('词云图生成成功！')
	img = Image.open('result.png')
	plt.figure()
	plt.imshow(img)
	plt.axis('off')
	plt.show()


if __name__ == '__main__':

	'''
	url = 'https://music.douban.com/top250'
	headers = {'User-Agent':'Mozilla/63.0,Chrome/70.0.3538.77'}
	response = requests.get(url,headers=headers)
	print(response.text)

	'''
	image_name = 'music.jpg'
	all_star = list()
	for i in range(0,250,25):
		url = 'https://music.douban.com/top250?start='+str(i)
		stars = get_result(url)
		time.sleep(0.1)
		all_star.extend(stars)
	
	with open('name.txt','a') as f:
		for name in all_star:
			f.write(name)
	
	create_wordcloud(all_star,image_name)