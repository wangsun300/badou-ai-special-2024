# 1.定义一个列表，并按照降序排列
my_list = [1,2,3,4,11,7,8,9]
my_list.sort(reverse=True)
print(my_list)


# 2.判断是否为偶数（分别用普通函数和匿名函数实现）
def isEvenNumber(key):
    return int(key) % 2 == 0
print(isEvenNumber(4))

result = lambda key: key % 2 == 0
print(result(35))


# 3.如何使用匿名函数对字典中的列表进行排序
my_list = [{'name':'zs','age':12},{'name':'ls','age':19}]
# print(my_list.sort(key=lambda x:x['age'],reverse=True))

def get_value(item):
    return item['age']

my_list.sort(key=get_value,reverse=True)
print(my_list)


# 4.利用Python进行文件拷贝
# 打开两个文件（源文件、目标文件）
old_file = open('./source.txt','rb')
new_file = open('./target.txt','wb')

# 文件操作
while True:
    # 1024: 读取1024字节的数据
    file_data = old_file.read(1024)
    # 判断数据是否读取完成
    if len(file_data) == 0:
        break
    new_file.write(file_data)

# 关闭文件流
old_file.close()
new_file.close()


# 5.面向对象的三大特征
# 继承、封装、多态


# 6.定义类class为Book,定义__init__函数和自定义函数，举例如: you(),info()
class Book():
    def __init__(self,name='爵迹',price=39,author='郭敬明'):
        self.name = name
        self.price = price
        self.author = author

    def you(self):
        print('努力学习%s图书' % self.name)

    def info(self):
        print('书籍名称：%s，价格：%s，作者：%s' % (self.name, self.price, self.author))

class Student(Book):
    pass

book = Book()
book.you()
book.__init__()

student = Student()
student.info()


# 7.使用正则表达式匹配全部字符串进行输出
# 源数据：abc  123  def
# 结 果： abc  123  def
import re

str2 = 'abc 123 def'
print(re.match('^abc\s\d\d\d\sdef$',str2).group())
print(re.match('^abc\s\d{3}\sdef$',str2).group())
print(re.match('^abc\s.*\sdef$',str2).group())
print(re.match('^abc\s(.*)\sdef$',str2).group())


# 8.使用正则表达式中sub实现获取我们匹配的字符串，然后追加指定字符
# 源数据：hello 7709 badou
# 结  果：hello 7709 badou
content = 'hello 7709 badou 23'
print(re.search('(\d+)',content).group(0))
print(re.search('(\d+)',content).group(1))
content = re.sub('(\d+)',r'\1 789',content)
print(content)
