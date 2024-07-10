from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from keras.utils import np_utils
from keras.optimizers import Adam
from model.AlexNet import AlexNet
import numpy as np
import utils
import cv2
from keras import backend as K
import os
# K.set_image_dim_ordering('tf')


def generate_arrays_from_file(lines, batch_size):
    n = len(lines)
    i = 0
    while 1:
        X_train = []
        Y_train = []
        for b in range(batch_size):
            if i == 0:
                np.random.shuffle(lines)
            name = lines[i].split(';')[0]
            path = os.path.join(r"第十一周\alexnet\data\image\train",name)
            # img = cv2.imread(r"第十一周\alexnet\data\image\train" + '/' + name)
            img = cv2.imdecode(np.fromfile(path),-1)
            # print("==========",img)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img = img / 255
            X_train.append(img)
            Y_train.append(lines[i].split(';')[1])
            i = (i + 1) % n
        X_train = utils.resize_image(X_train, (224,224))
        X_train = X_train.reshape(-1, 224,224,3)
        Y_train = np_utils.to_categorical(np.array(Y_train), num_classes=2)
        yield (X_train, Y_train)

if __name__ == "__main__":
    log_dir = r"第十一周\alexnet\logs"

    with open(r"第十一周\alexnet\data\dataset.txt","r") as f:
        lines = f.readlines()

    np.random.seed(10101)
    np.random.shuffle(lines)
    np.random.seed(None)

    num_val = int(len(lines) * 0.1)
    num_train = len(lines) - num_val

    model = AlexNet()

    checkpoint_period1 = ModelCheckpoint(
        log_dir + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
                                         monitor='acc',
                                         save_weights_only=False,
                                         save_best_only=True,
                                         period=3)
    
    reduce_lr = ReduceLROnPlateau(
        monitor='acc',
        factor=0.5,
        patience=3,
        verbose=1
    )

    early_stopping = EarlyStopping(
        monitor='val_loss',
        min_delta=0,
        patience=10,
        verbose=1
    )

    model.compile(
        loss='categorical_crossentropy',
        optimizer= Adam(lr=1e-3),
        metrics=['accuracy']
    )

    batch_size = 128

    print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))

    model.fit_generator(
        generate_arrays_from_file(lines[:num_train], batch_size),
        steps_per_epoch=max(1,num_train//batch_size),
        validation_data=generate_arrays_from_file(lines[num_train:], batch_size),
        validation_steps=max(1, num_val//batch_size),
        epochs=50,
        initial_epoch=0,
        callbacks=[checkpoint_period1, reduce_lr]
    )

    model.save_weights(log_dir+'last.h5')