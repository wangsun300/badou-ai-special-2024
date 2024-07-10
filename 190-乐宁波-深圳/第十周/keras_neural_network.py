# 读取训练数据
from keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print('train_images.shape = ', train_images.shape)
print('train_labels.shape = ', train_labels.shape)
print('test_images.shape = ', test_images.shape)
print('test_labels.shape = ', test_labels.shape)

# 打印一张图
# digit = test_images[123]
import matplotlib.pyplot as plt
#
# plt.imshow(digit, cmap=plt.cm.binary)
# plt.show()

# 构建神经网络
from keras import models
from keras import layers

# 一个线性堆叠的层结构，用于构建一个按顺序添加层的神经网络
network = models.Sequential()

# network.add表示给神经网络加一层
# layers.Dense表示一个全连接层
# activation表示激活函数
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(10, activation='softmax'))

from keras.optimizers import RMSprop

# RMSprop是一种优化算法
optimizer = RMSprop(learning_rate=0.01)
# categorical_crossentropy是交叉熵损失函数
# metrics是指定一个指标，在训练过程中，模型会计算并输出epoch的训练集和验证集的准确率
network.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# 数据格式处理
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

from keras.utils import to_categorical

print("before change:", test_labels[0])
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
print("after change: ", test_labels[0])
# 训练
network.fit(train_images, train_labels, epochs=5, batch_size=100)

# 测试
test_loss, test_acc = network.evaluate(test_images, test_labels, verbose=1)
print('test_loss', test_loss)
print('test_acc', test_acc)

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
digit = test_images[1234]
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()
test_images = test_images.reshape((10000, 28 * 28))
res = network.predict(test_images)

for i in range(res[1234].shape[0]):
    if (res[1234][i] == 1):
        print("the number for the picture is : ", i)
        break
