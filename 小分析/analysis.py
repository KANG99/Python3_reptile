import matplotlib.pyplot as plt
from wordcloud import WordCloud
from imageio import imread
from PIL import Image
import numpy as np 


def create_wordcloud(image_name,contents):
	
	authors = ' '
	for content in contents: #遍历所有作者名字，将所有名字组成字符串
		content = eval(content)
		#print(content)
		author = content['作者']
		author += ' '
		authors += author
	bg = imread(image_name) #读取背景图片
	wc = WordCloud(font_path='msyhbd.ttc',background_color='white',
					max_words=2000,mask=bg,random_state=200)#词云图对象：设置字体，背景颜色，最大词数，背景图片，
	wc.generate(authors) #根据字符串生成词云图
	#image_colors = ImageColorGenerator(bg)
	wc.to_file('result.png')#保存词云图图片
	print('成功生成词云图')
	
	img = Image.open('result.png')#打开词云图图片
	plt.figure(figsize=(10,10))#设置展示窗口大小
	plt.imshow(img)#显示的图片
	plt.axis('off')#关闭坐标轴
	plt.show(img)#显示图片（因为图像的内部数据还是浮点数造成的，正常显示需要添加这一句）

def figure_show(x,y,color='dodgerblue',title='浏览次数排行',legend='views'):

	plt.figure(figsize=(15,6)) #设置窗口大小15x6
	plt.rcParams['font.sans-serif']=['SimHei']
	#plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
	rects = plt.bar(x,y,color=color) #生成条形图
	plt.plot(x,y) #生成折线图
	plt.legend([legend],fontsize=10)#设置图例
	font = {'style':'normal','size':10} #设置字体风格，大小
	for rect in rects: #遍历所有的条形图
		height = rect.get_height()#获取每个条形图的高度
		plt.text(rect.get_x() + rect.get_width()*0.5,1.01*height,str(height),fontdict=font)#将文本内容显示在条形图适当位置
	plt.xticks(fontsize=7)#设置x,y坐标刻度字体大小
	plt.yticks(fontsize=7)
	plt.title(title)#添加图表标题
	plt.show()#显示图片

def create_views_bar(contents):
	'''
	因为获取得到的数据是字符串，利用eval将字符串转换为字典类型
	数据根据浏览次数排序的，所以将前10的浏览次数和作者名+作品名
	依次添加到列表中
	图表中作者名+作品作为横轴，浏览数作为纵轴数据显示
	'''
	authors_works = []
	total_views = []
	for content in contents[:10]:
		content = eval(content)
		author = content['作者']
		work = content['作品']
		author_work = author + '\n' + work
		authors_works.append(author_work)
		total_views.append(content['浏览次数'])
	
	figure_show(authors_works,total_views)#生成可视化窗口


def price_point_bar(contents):
	'''
	因为数据是按浏览数排行的，所以要再次对点赞数进行排序，并找到点赞数相应相应的作者和作品，
	在图表中作者名+作品作为横轴，点赞数作为纵轴
	'''
	total_price_points = []
	for content in contents:
		content = eval(content)
		total_price_points.append(content['点赞次数'])
	total_price_points.sort(reverse=True)
	
	total_price_points = total_price_points[:10]
	authors_works = []
	for point in total_price_points:
		for content in contents:
			content = eval(content)
			if point == content['点赞次数']:
				authors_works.append(content['作者']+'\n'+content['作品'])
				break

	figure_show(authors_works,total_price_points,color='green',title='点赞次数排行',legend='pricePoint')


def create_rate_bar(contents):
	'''
	找出浏览数为不小于10000的作品，进行点赞率计算，结果保留4位位数字
	找出点赞率前10的作者和作品作为横轴，点赞率作为纵轴

	'''
	rate_dict = {}
	rates = []
	authors_works = []
	for content in contents:
		content = eval(content)
		views = content['浏览次数'] 
		price_points = content['点赞次数']
		author = content['作者']
		work = content['作品']
		if views >= 10000:
			rate_dict[author+'\n'+work] = round(price_points/views,4)
	for key,value in rate_dict.items():
		rates.append(value)
	rates.sort(reverse=True)
	rates = rates[:10]
	
	for rate in rates:
		for key,value in rate_dict.items():
			if rate == value:
				authors_works.append(key)
				break
	
	figure_show(authors_works,rates,color='tomato',title='点赞率排行榜',legend='rates')

def create_num_pie(contents):
	
	'''
	绘制浏览数大于10000,10000~5000,1000~5000，小于1000四个区间人数分布
	可以发现浏览数小于1000的作品很多，新生市场有活力
	'''
	views = []
	for content in contents:
		content = eval(content)
		views.append(content['浏览次数'])
	views.sort()
	a = len([i for i in views if i >= 10000])
	b = len ([i for i in views if i >= 5000]) - a
	c = len ([i for i in views if i >= 1000]) - a -b 
	d = len(views) - a - b - c 
	nums = [a,b,c,d]
	explode = [0,0,0,0.05]
	labels = ['A>=10000', '10000>B>=5000', '5000>C>=1000', '1000>D']
	plt.rcParams['font.sans-serif']=['SimHei']
	plt.figure(figsize=(10,10))
	plt.axes(aspect=1) #这样子设置饼才是圆的，否则椭圆
	plt.pie(nums,labels=labels,explode=explode,autopct='%3.1f%%',shadow=True, labeldistance=1.1, startangle = 90,pctdistance = 0.6)
	plt.title('浏览次数分布')
	plt.show()



if __name__ == '__main__':


	with open("kitten作品信息.txt",'r',encoding='utf-8') as f:
		contents = f.readlines()
	#create_wordcloud('猫老祖.png',contents)
	create_views_bar(contents)
	#price_point_bar(contents)
	#create_rate_bar(contents)
	#create_num_pie(contents)




	

	
	
	



