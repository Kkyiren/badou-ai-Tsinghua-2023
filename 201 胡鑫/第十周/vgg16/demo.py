import tensorflow as tf
import utils
from nets import vgg16

# 读取图片
img1 = utils.load_image("./test/table.jpg")

# 对输入的图片进行resize，使其满足(-1, 224, 224, 3)
inputs = tf.placeholder(tf.float32, [None, None, 3])
resized_img = utils.resize_image(inputs, (224, 224))

# 建立网络结构
prediction = vgg16.vgg_16(resized_img)

# 载入模型
sess = tf.Session()
ckpt_filename = './model/vgg_16.ckpt'
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
saver.restore(sess, ckpt_filename)

# 最后结果进行softmax预测
pro = tf.nn.softmax(prediction)
pre = sess.run(pro, feed_dict={inputs: img1})

print("result: ")
utils.print_prob(pre[0], './synset.txt')



