from bs4 import BeautifulSoup
import requests
import cv2
import os
import time
'''
本次任务利用requests请求获取豆瓣美女图片，beautifulsoup对请求的网页进行解析，
利用opencv对图片进行人脸识别，剔除非人脸的图片
'''
#使用BeautifulSoup对网页进行解析
def get_image_urls(url):
	headers = {'User-Agent':'Mozilla/63.0,Chrome/70.0.3538.77'}
	data = requests.get(url,headers=headers)
	data = data.text
	#print(data)
	soup = BeautifulSoup(data,'lxml')
	img_urls = soup.find_all(name='img')
	#print(soup.img.attrs['src'])
	urls = []
	for img_data in img_urls:
		urls.append(img_data.attrs['src'])
	return urls

def is_face(filename):

	image = cv2.imread(filename)
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#分类器添加训练后的文件
	face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
	# 探测人脸
	# 根据训练的数据来对新图片进行识别的过程。
	faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.15,minNeighbors = 5,minSize = (5,5))

	return bool(len(faces))

if __name__ == '__main__':
	
	n = 0
	headers = {'User-Agent':'Mozilla/63.0,Chrome/70.0.3538.77'}
	for i in range(1,11):
		url = 'https://www.dbmeinv.com/index.htm?pager_offset='+str(i)
		urls = get_image_urls(url)
		for img_url in urls:
			reponse = requests.get(img_url,headers=headers)
			path = 'img/'+'beauty'+str(n)+'.jpg'
			with open(path,'wb') as f:
				f.write(reponse.content)
			print('爬取第%d张图片成功，进行检测……'%n)
			if not is_face(path):
				os.remove(path)
			n += 1
		time.sleep(0.1)
