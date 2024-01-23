from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import plot_model
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from PIL import Image
import tensorflow as tf

class MultiClassNetworkTrainer:
    def __init__(self):
        pass

    def create_model(self, input_shape, nclasses, loss_type, activation_fun, dropout_rate, learning_rate):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(256, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation('relu'))
        model.add(Dense(500))
        model.add(Activation('relu'))
        model.add(Dropout(dropout_rate))
        model.add(Dense(nclasses))
        model.add(Activation(activation_fun))
        opt = optimizers.Adam(lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
        model.compile(loss=loss_type, optimizer=opt, metrics=['accuracy'])
        return model

    def train_multi_class_network(self, source_dir, target_dir, project_path, project_name, plot_path):
        train_data_dir = os.path.join(target_dir, 'training')
        validation_data_dir = os.path.join(target_dir, 'validation')

        t = []
        v = []
        for t_file in glob.iglob(train_data_dir + '/**/*.jpg', recursive=True):
            t.append(t_file)
        for v_file in glob.iglob(validation_data_dir + '/**/*.jpg', recursive=True):
            v.append(v_file)
        t_l = len(t)
        v_l = len(v)

        path = source_dir
        classes = os.listdir(path)
        cnt_list = [len(list(glob.iglob(os.path.join(path, cl) + '/**/*.jpg', recursive=True))) for cl in classes]
        w_list = [(1 / i) * (sum(cnt_list) / len(cnt_list)) for i in cnt_list]
        weights = {i: w for i, w in enumerate(w_list)}

        img_height, img_width = Image.open(t[0]).size
        epochs = 50
        batch_size = 15
        nclasses = len(classes)
        loss_type = 'categorical_crossentropy'
        class_type = 'categorical'
        activation_fun = 'softmax'
        nb_train_samples = t_l
        nb_validation_samples = v_l
        learning_rate = 0.00015
        dropout_rate = 0.5
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.000005)
        early = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='min')

        input_shape = (img_height, img_width, 3)
        model = self.create_model(input_shape, nclasses, loss_type, activation_fun, dropout_rate, learning_rate)

        callbacks = [early, reduce_lr]

        train_datagen = ImageDataGenerator(rescale=1. / 255)
        validation_datagen = ImageDataGenerator(rescale=1. / 255)

        train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=(img_height, img_width),
            batch_size=batch_size,
            class_mode=class_type)

        validation_generator = validation_datagen.flow_from_directory(
            validation_data_dir,
            target_size=(img_height, img_width),
            batch_size=batch_size,
            class_mode=class_type)

        history = model.fit_generator(
            train_generator,
            steps_per_epoch=nb_train_samples // batch_size,
            epochs=epochs,
            class_weight=weights,
            callbacks=callbacks,
            validation_data=validation_generator,
            validation_steps=nb_validation_samples // batch_size)

        project = os.path.join(project_path, project_name)
        model.save(os.path.join(project, project_name) + '.h5')

        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper left')
        plt.savefig(os.path.join(plot_path, 'accuracy.png'))
        plt.close()

        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper left')
        plt.savefig(os.path.join(plot_path, 'loss.png'))
        plt.close()

# Example Usage:
# multi_class_trainer = MultiClassNetworkTrainer()
# multi_class_trainer.train_multi_class_network('source_directory', 'target_directory', 'project_path', 'project_name', 'plot_path')
