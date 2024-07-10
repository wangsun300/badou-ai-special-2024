import tensorflow as tf
import numpy as np
import time
import math
import Cifar10_data

# 设置训练参数
max_steps = 4000
batch_size = 100
num_examples_for_eval = 10000
data_dir = "Cifar_data/cifar-10-batches-bin"

# 定义一个函数，用于创建具有L2正则化的权重变量
def variable_with_weight_loss(shape, stddev, w1):
    var = tf.Variable(tf.truncated_normal(shape, stddev=stddev))
    if w1 is not None:
        weights_loss = tf.multiply(tf.nn.l2_loss(var), w1, name="weights_loss")
        tf.add_to_collection("losses", weights_loss)
    return var

# 读取训练和测试数据，训练数据进行数据增强，测试数据不进行数据增强
images_train, labels_train = Cifar10_data.inputs(data_dir=data_dir, batch_size=batch_size, distorted=True)
images_test, labels_test = Cifar10_data.inputs(data_dir=data_dir, batch_size=batch_size, distorted=None)

# 定义输入数据和标签的占位符
x = tf.placeholder(tf.float32, [batch_size, 24, 24, 3])
y_ = tf.placeholder(tf.int32, [batch_size])

# 创建第一个卷积层
kernel1 = variable_with_weight_loss(shape=[5, 5, 3, 64], stddev=5e-2, w1=0.0)
conv1 = tf.nn.conv2d(x, kernel1, [1, 1, 1, 1], padding="SAME")
bias1 = tf.Variable(tf.constant(0.0, shape=[64]))
relu1 = tf.nn.relu(tf.nn.bias_add(conv1, bias1))
pool1 = tf.nn.max_pool(relu1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding="SAME")

# 创建第二个卷积层
kernel2 = variable_with_weight_loss(shape=[5, 5, 64, 64], stddev=5e-2, w1=0.0)
conv2 = tf.nn.conv2d(pool1, kernel2, [1, 1, 1, 1], padding="SAME")
bias2 = tf.Variable(tf.constant(0.1, shape=[64]))
relu2 = tf.nn.relu(tf.nn.bias_add(conv2, bias2))
pool2 = tf.nn.max_pool(relu2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding="SAME")

# 展平池化层的输出，以便连接全连接层
reshape = tf.reshape(pool2, [batch_size, -1])
dim = reshape.get_shape()[1].value

# 创建第一个全连接层
weight1 = variable_with_weight_loss(shape=[dim, 384], stddev=0.04, w1=0.004)
fc_bias1 = tf.Variable(tf.constant(0.1, shape=[384]))
fc_1 = tf.nn.relu(tf.matmul(reshape, weight1) + fc_bias1)

# 创建第二个全连接层
weight2 = variable_with_weight_loss(shape=[384, 192], stddev=0.04, w1=0.004)
fc_bias2 = tf.Variable(tf.constant(0.1, shape=[192]))
local4 = tf.nn.relu(tf.matmul(fc_1, weight2) + fc_bias2)

# 创建第三个全连接层，输出层
weight3 = variable_with_weight_loss(shape=[192, 10], stddev=1 / 192.0, w1=0.0)
fc_bias3 = tf.Variable(tf.constant(0.1, shape=[10]))
result = tf.add(tf.matmul(local4, weight3), fc_bias3)

# 计算交叉熵损失，并加入L2正则化损失
cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=result, labels=tf.cast(y_, tf.int64))
weights_with_l2_loss = tf.add_n(tf.get_collection("losses"))
loss = tf.reduce_mean(cross_entropy) + weights_with_l2_loss

# 使用Adam优化器最小化损失
train_op = tf.train.AdamOptimizer(1e-3).minimize(loss)

# 计算模型在top 1上的准确率
top_k_op = tf.nn.in_top_k(result, y_, 1)

# 初始化所有变量
init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init_op)
    tf.train.start_queue_runners()

    # 每100步打印一次损失和训练速度
    for step in range(max_steps):
        start_time = time.time()
        image_batch, label_batch = sess.run([images_train, labels_train])
        _, loss_value = sess.run([train_op, loss], feed_dict={x: image_batch, y_: label_batch})
        duration = time.time() - start_time

        if step % 100 == 0:
            examples_per_sec = batch_size / duration
            sec_per_batch = float(duration)
            print("step %d, loss=%.2f (%.1f examples/sec; %.3f sec/batch)" % (step, loss_value, examples_per_sec, sec_per_batch))

    # 计算模型在测试集上的准确率
    num_batch = int(math.ceil(num_examples_for_eval / batch_size))
    true_count = 0
    total_sample_count = num_batch * batch_size

    for j in range(num_batch):
        image_batch, label_batch = sess.run([images_test, labels_test])
        predictions = sess.run([top_k_op], feed_dict={x: image_batch, y_: label_batch})
        true_count += np.sum(predictions)

    # 打印准确率
    print("accuracy = %.3f%%" % ((true_count / total_sample_count) * 100))
