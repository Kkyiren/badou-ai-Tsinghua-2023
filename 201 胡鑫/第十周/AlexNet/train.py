from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from keras.utils import np_utils
from keras.optimizers import Adam
from model.AlexNet import AlexNet
import numpy as np
import utils
import cv2
from keras import backend as k
import time

k.set_image_data_format("channels_last")


def generate_arrays_from_file(lines, batch_size):
    # 获取总长度
    n = len(lines)
    i = 0
    while True:
        x_train = []
        y_train = []
        # 获取一个batch_size大小的数据
        for b in range(batch_size):
            if i == 0:
                np.random.shuffle(lines)
            name = lines[i].split(';')[0]
            # 从文件中读取图像
            img = cv2.imread(r"./data/image/train/" + name)
            # 图像数据简单预处理
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img / 255
            x_train.append(img)
            y_train.append(lines[i].split(';')[1])
            # 读完一个周期后重新开始
            i = (i + 1) % n
        # 处理图像
        x_train = utils.resize_image(x_train, (224, 224))
        x_train = x_train.reshape(-1, 224, 224, 3)
        y_train = np_utils.to_categorical(np.array(y_train), num_classes=2)
        yield x_train, y_train


if __name__ == '__main__':
    start_time = time.time()
    # 模型保存的位置
    log_dir = "./logs/"

    # 打开数据集的txt
    with open(r"./data/dataset.txt", "r") as f:
        lines = f.readlines()

    # 打乱顺序，这个txt主要用于帮助读取数据来训练
    # 打乱的数据更有利于训练
    np.random.seed(10101)
    np.random.shuffle(lines)
    np.random.seed(None)

    # 90%用于训练，10%用于估计
    num_val = int(len(lines) * 0.1)
    num_train = len(lines) - num_val

    # 建立AlexNet模型
    model = AlexNet()

    # 保存的方式，三代保存一次
    checkpoint_period1 = ModelCheckpoint(
        log_dir + 'ep{epoch:03d} - loss{loss:.3f} - val_loss{val_loss:.3f}.h5',
        monitor='acc',
        save_weights_only=False,
        save_best_only=True,
        period=3
    )

    # 学习率下降的方式，acc三次不下降就下降学习率继续训练
    reduce_lr = ReduceLROnPlateau(
        monitor='acc',
        factor=0.5,
        patience=3,
        verbose=1
    )

    # 是否需要早停，当val_loss一直不下降的时候意味着模型基本训练完毕，可以停止
    early_stopping = EarlyStopping(
        monitor='val_loss',
        min_delta=0,
        patience=10,
        verbose=1
    )

    # 交叉熵
    model.compile(
        loss='categorical_crossentropy',
        optimizer=Adam(lr=1e-3),
        metrics=['accuracy']
    )

    # 一次的训练集大小
    batch_size = 128
    print(f"Train on {num_train} samples, val on {num_val} samples, with batch size {batch_size}")

    # 开始训练
    model.fit_generator(
        generate_arrays_from_file(lines[:num_train], batch_size),
        steps_per_epoch=max(1, num_train // batch_size),
        validation_data=generate_arrays_from_file(lines[num_train:], batch_size),
        validation_steps=max(1, num_val // batch_size),
        epochs=50,
        initial_epoch=0,
        callbacks=[checkpoint_period1, reduce_lr]
    )
    model.save_weights(log_dir + "last1.h5")
    print(time.time() - start_time)
