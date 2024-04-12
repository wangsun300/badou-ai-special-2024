# 通过用户输入两个数字，并计算两个数字之和
try:
    a = int(input('请输入第一个数字：'))
except ValueError:
    print('请输入数字类型的数据')
else:
    try:
        b = int(input('请输入第二个数字：'))
    except ValueError:
        print('请输入数字类型的数据')
    else:
        print('%d + %d = %d'%(a,b,a+b))

# 生成随机数
import random
num = random.randint(1,100)
print(num)

# 生成九九乘法表的三种方法
for x in range(1,10):
    for y in range(1,x+1):
        print("%d*%d=%d" % (y, x, x * y), end=" ")
    print('')

for x in range(1,10):
    y = 1
    while y <= x:
        print('%d*%d=%d' % (y, x, x * y), end=" ")
        y += 1
    print('')

# 一行代码实现九九乘法表
print('一行代码实现九九乘法表')
print('\n'.join(['\t'.join(['%d*%d=%d' % (j,i,j*i) for j in range(1,i+1)]) for i in range(1,10)]))
