import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import cv2
from sklearn import svm, metrics
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from keras.utils.vis_utils import plot_model


def train_neural_net(x_data, y_data, neural_net_name):
    x_shuffled, y_shuffled = shuffle(x_data, y_data)
    x_train, y_train = x_shuffled[0:int(0.8 * len(x_shuffled))], y_shuffled[0:int(0.8 * len(y_shuffled))]
    x_test, y_test = x_shuffled[int(0.8 * len(x_shuffled)):], y_shuffled[int(0.8 * len(y_shuffled)):]

    # fetch train and test MNIST data
    # (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
    # normalize
    x_train = x_train / 255.0
    x_test = x_test / 255.0

    # visualize 1 example
    plt.imshow(x_test[7])
    plt.show()

    # possible targets count and input shape
    num_classes = 10
    input_shape = (28, 28, 1)

    # expand the shape of an array (add a new axis)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    # change target to categorical
    y_train = tf.keras.utils.to_categorical(y_train, num_classes)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes)

    print(x_train.shape)

    # file with trained neural net
    path_to_neural_net = neural_net_name

    # load if saved; create and train otherwise
    if not os.path.isfile(path_to_neural_net):

        # create neural net model
        model = tf.keras.Sequential(
            [
                tf.keras.Input(shape=input_shape),
                tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
                tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(num_classes, activation='softmax'),
            ]
        )
        model.summary()

        # train
        batch_size = 128
        epochs = 100
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

        # save
        model.save(path_to_neural_net)

        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('Точность нейросети')
        plt.ylabel('Точность')
        plt.xlabel('Номер эпохи')
        plt.legend(['обучение', 'валидация'], loc='upper left')
        plt.show()

        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Функция потерь')
        plt.ylabel('Потери')
        plt.xlabel('Номер эпохи')
        plt.legend(['обучение', 'валидация'], loc='upper left')
        plt.show()

    else:
        # load model
        model = tf.keras.models.load_model(path_to_neural_net)

    # evaluate
    score = model.evaluate(x_test, y_test, verbose=0)
    print(f'Test loss: {score[0]}')
    print(f'Test accuracy: {score[1]}')

    print(model.predict(np.array([x_test[7]])))
    print([np.argmax(el) for el in model.predict(np.array(x_test))])
    print(y_data)
    conf_matrix_disp = metrics.ConfusionMatrixDisplay.from_predictions(y_data, [str(np.argmax(el)) for el in
                                                                                model.predict(
                                                                                    np.array(x_data))])
    conf_matrix_disp.figure_.suptitle('Confusion Matrix (train + test)')
    plt.show()
    plot_model(model, to_file='../images/model_plot.jpg', show_shapes=True, show_layer_names=True)
    print(model.summary())


def train_svc(x_data, y_data, classifier_name):
    x_data = x_data.reshape((len(x_data), -1))
    clf = svm.SVC(gamma=0.07)
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.5)
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    clf.fit(x_train, y_train)
    predicted = clf.predict(x_test)
    conf_matrix_disp = metrics.ConfusionMatrixDisplay.from_predictions(y_test, predicted)
    conf_matrix_disp.figure_.suptitle('Confusion Matrix')
    plt.show()


if __name__ == '__main__':
    all_files = os.listdir('../ml_model/dataset/')
    reg_pattern = re.compile(r'\d_\d+.jpeg')
    filtered_files = [i for i in all_files if reg_pattern.match(i)]

    X = []
    y = []

    for file in filtered_files:
        X.append(cv2.imread('../ml_model/dataset/' + file, cv2.IMREAD_GRAYSCALE))
        y.append(file[0])
    X = np.array(X)
    y = np.array(y)

    train_neural_net(X, y, 'neural_net_classifier_2.h5')
    # train_svc(X, y, 'support_vector_classifier_1.h5')
