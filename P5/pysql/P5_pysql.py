import pymysql
import requests
from pyquery import PyQuery as pq 

try:
	sql = 'DROP TABLE zhihu'
	cursor.execute(sql)
	db.commit()
except:
	print('no table name zhihu')

db = pymysql.connect(host='localhost',user='root',password='123456',port=3306,db='spiders')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS zhihu(questions MEDIUMTEXT NOT NULL, answers MEDIUMTEXT NOT NULL)'
cursor.execute(sql)

url = 'https://www.zhihu.com/explore'
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
html = requests.get(url,headers=headers).text
# html = etree.HTML(html)
# html = etree.tostring(html).decode('utf-8')
#print(html)
doc = pq(html)
items = doc('.ExploreRoundtableCard-questionItem ').items()
for item in items:
	answers = ' '
	Dict = {}
	question = item.find('.ExploreRoundtableCard-questionTitle').text()
	# with open('zhihu.txt','a',encoding='utf-8') as f:
	# 		f.write(question+'\n')
	Dict['questions'] = question
	info = item.find('.ExploreRoundtableCard-questionTitle').attr.href
	anwser_url = 'https://www.zhihu.com'+info
	#print(anwser_url)
	html = requests.get(anwser_url,headers=headers)
	doc = pq(html.text)
	anwser_items = doc('.RichContent-inner').items()
	#print(anwser_items)
	for anwser_item in anwser_items:
		# with open('zhihu.txt','a',encoding='utf-8') as f:
		# 	f.write(anwser_item.text()+'\n')
		answers += anwser_item.text()+'\n'
	#print(answers)
	Dict['answers'] = answers
	Dict = Dict.copy()
	keys = ','.join(Dict.keys())
	values = ','.join(['%s']*len(Dict))
	sql = 'INSERT INTO zhihu({keys}) VALUES({values})'.format(keys=keys,values=values)
	try:
		print(sql)
		cursor.execute(sql,tuple(Dict.values()))
		db.commit()
		print('Successful!')
	except:
		print('Failed!')

sql = 'SELECT * FROM zhihu'
try:
	cursor.execute(sql)
	question,answer = cursor.fetchone()
	while question:
		print(question)
		print('='*50)
		print(answer)
		print('='*50)
		question,answer = cursor.fetchone()
except:
	print('Errors',answer)
db.close()

# cursor.execute('SELECT VERSION()')
# data = cursor.fetchone()
# print('Database version:',data)
# cursor.execute('CREATE DATABASE spiders DEFAULT CHARACTER SET utf8')

# cursor.execute('CREATE TABLE IF NOT EXISTS students(id varchar(255) NOT NULL, name varchar(255) NOT NULL, age int NOT NULL, PRIMARY KEY (id))')
# print(cursor.execute('SHOW TABLES'))
# print(cursor.execute('SELECT * FROM students'))
# data= {'id' : '20120003',
# 	'name' : 'miky',
# 	'age' : 21}
# keys = ', '.join(data.keys())
# values = ', '.join(['%s']*len(data))
# sql = 'INSERT INTO students({keys}) VALUES({values}) ON DUPLICATE KEY UPDATE '.format(keys=keys,values=values)
# update = ','.join(['{key}=%s'.format(key=key) for key in data])
# sql += update
#condition = 'age > 20'
#sql = 'DELETE FROM students WHERE {}'.format(condition)
# sql = 'SELECT * FROM students'
# try:
	#print(sql)
	#cursor.execute(sql,tuple(data.values())*2)
# 	cursor.execute(sql)
# 	#all = cursor.fetchall()
# 	print('Successful')
# 	#print(all)
# 	#db.commit()
# 	row = cursor.fetchone()
# 	while row:
# 		print(row)
# 		row = cursor.fetchone()
# except:
# 	print('Failed')
# 	db.rollback()
# db.close()
