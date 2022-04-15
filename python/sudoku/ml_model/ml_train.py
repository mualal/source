import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import cv2
from sklearn.utils import shuffle

all_files = os.listdir('../ml_model/dataset/')
reg_pattern = re.compile(r'\d_\d+.jpeg')
filtered_files = [i for i in all_files if reg_pattern.match(i)]

X = []
y = []

for file in filtered_files:
    X.append(cv2.imread('../ml_model/dataset/'+file, cv2.IMREAD_GRAYSCALE))
    y.append(file[0])
X = np.array(X)
y = np.array(y)

X, y = shuffle(X, y)
X_train, y_train = X[0:int(0.8*len(X))], y[0:int(0.8*len(y))]
X_test, y_test = X[int(0.8*len(X)):], y[int(0.8*len(y)):]

# fetch train and test MNIST data
# (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
# normalize
X_train = X_train / 255.0
X_test = X_test / 255.0

# visualize 1 example
plt.imshow(X_test[7])
plt.show()

# possible targets count and input shape
num_classes = 10
input_shape = (28, 28, 1)

# expand the shape of an array (add a new axis)
X_train = np.expand_dims(X_train, -1)
X_test = np.expand_dims(X_test, -1)

# change target to categorical
y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)

print(X_train.shape)

# file with trained neural net
path_to_neural_net = 'printed_digit_recognition_net.h5'

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
    epochs = 55
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

    # save
    model.save('printed_digit_recognition_net.h5')
else:
    # load model
    model = tf.keras.models.load_model(path_to_neural_net)

# evaluate
score = model.evaluate(X_test, y_test, verbose=0)
print(f'Test loss: {score[0]}')
print(f'Test accuracy: {score[1]}')

print(model.predict(np.array([X_test[7]])))
