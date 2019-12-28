import pymongo

#链接MongoDB
client = pymongo.MongoClient(host='localhost',port=27017)
#client = MongoClient('mongodb://localhost:27017')
#指定名为test的数据库
db = client.test
#db= client['test']
#指定集合，每个数据库里面存在的集合类似关系型数据库中表,调用名为students的集合
collection = db.students
#collection = db['students']
#MongoDB每条数据其实都有一个_id来唯一标识，如果没有指明该属性，MongoDB会自动产生一个ObjectID类型的_id属性
#利用集合的insert方法插入数据,insert()方法在执行后返回_id值
student = {
	'id':'20170101',
	'name':'Jordan',
	'age':20,
	'gender':'male'
}
result = collection.insert(student)
print(result)
#可以将插入的对象放入到列表中，同时插入多条数据
student1 = {
	'id':'20170102',
	'name':'Kobe',
	'age':19,
	'gender':'male'
}
student2 = {
	'id':'20170103',
	'name':'James',
	'age':19,
	'gender':'male'
}
results = collection.insert([student1,student2])
print(results)
#python官方不推荐使用insert()方法插入数据，推荐insert_one()和insert_many()方法插入单条数据和多条数据
#insert_one()和insert_many()方法分别是InsertOneResult和InsertManyResult对象
student3 = {
	'id':'20170104',
	'name':'Rose',
	'age':18,
	'gender':'male'
}
result = collection.insert_one(student3)
print(result)
print(result.inserted_id)
#使用insert_many()方法
student4 = {
	'id':'20170105',
	'name':'Alice',
	'age':17,
	'gender':'female'
}
student5 = {
	'id':'20170106',
	'name':'Lucy',
	'age':17,
	'gender':'female'
}
results = collection.insert_many([student4,student5])
print(results)
print(results.inserted_ids)
#利用find_one()或者是find方法进行数据查询，find_one()查询得到单个结果
result = collection.find_one({'name':'Kobe'})
print(type(result))
print(result)
#利用find()返回一个cursor对象相当于生成器对象
results = collection.find({'age':20})
print(results)
for result in results:
	print(result)
#通过比较运算符查询符合一定范围的内容
results = collection.find({'age':{'$in':[18,19]}})
for result in results:
	print(result)
'''
						比较符号
=================================================================
符号                     含义                    实例
$lt                     小于                  {"age":{"$lt":20}}

$gt                     大于					  {"age":{"$gt":20}}

$lte                   小于等于				  {"age":{"$lte":20}}

$gte                   大于等于				  {"age":{"$gte":20}}


$ne                    不等于				  {"age":{"$ne":20}}

$in                   在范围内				  {"age":{"$in":[18,20]}}

$nin                   不在范围内			  {"age":{"$nin":[18,20]}}

=================================================================

'''
#通过正则匹配查询
results = collection.find({'name':{'$regex':'^M.*'}})
for result in results:
	print(result)
'''
						功能符号
========================================================================================================
符号                     含义                    实例									示例含义
$regex            匹配正则表达式               {"name":{"$regex":"^M.*"}}          name以M开头

$exists           属性是否存在				  {"name":{"$exists":True}}			  name属性存在

$type             类型判断				      {"age":{"$type":int}}				age的类型为int

$mod              数字模操作			 		  {"age":{"$mod":[5,0]}}			  年龄模5余0

$text             文本查询				 	  {"$text":{"$search":'Kobe'}}    text类型的属性中包含Kobe的字符串  

$where            高级条件查询

========================================================================================================

'''
#计数，统计查询结果有多少条数据，使用count方法进行查询
count = results.count()
print(count)

#排序,利用sort方法，进行排序，传入升降序标识符(升序 ASCENDING 降序 DESCENDING)
results = collection.find().sort('name',pymongo.ASCENDING)
print([result['name'] for result in results])

#偏移,skip()方法偏移几个位置,用limit方法来限定要取出的结果个数
results = collection.find().sort('name,pymongo.ASCENDING').skip(2)
print([result['name'] for result in results])

results = collection.find().sort('name,pymongo.ASCENDING').skip(2).limit(2)
print([result['name'] for result in results])

#更新,使用update方法，指定更新的条件和更新后的数据
condition = {"name":"James"}
student6 = collection.find_one(condition)
print(student6)
student6['age'] = 22
result = collection.update(condition,student6)
print(result)
student6 = collection.find_one(condition)
print(student6)
#可以使用$set操作符对数据进行更新，只更新student字典内存在的字段。,官方推荐使用update_one和update_many方法更新数据
condition = {"name":"James"}
student6 = collection.find_one(condition)
print(student6)
student6['age'] = 23
result = collection.update_one(condition,{'$set':student6})
print(result)
print(result.matched_count,result.modified_count)
student6 = collection.find_one(condition)
print(student6)
#update_many
condition = {'age':{'$gt':20}}
students = collection.find(condition)
print(students)
result = collection.update_many(condition,{'$inc':{'age':1}})
print(result)
print(result.matched_count,result.modified_count)
students = collection.find(condition)
print(students)

#删除,remove方法指定删除条件，官方推荐使用delete_one()和delete_many()方法
students = collection.find()
for student in students:
	print(student)
result = collection.remove({'name':'Kobe'})
print(result)
students = collection.find()
print(students)
result = collection.delete_many({'age':{'$lt':25}})
print(result.deleted_count)
students = collection.find()
print(students)
#其他操作