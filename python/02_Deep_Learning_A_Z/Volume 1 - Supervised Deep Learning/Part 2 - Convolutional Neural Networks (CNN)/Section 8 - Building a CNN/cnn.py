# Convolutional Neural Network

# Installing Theano
# pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git

# Installing Tensorflow
# pip install tensorflow

# Installing Keras
# pip install --upgrade keras

# Preprocessing part is done as part of segregating the images into separte
#  folders as training_set and test_test, jumping to building part directly

# Part 1 - Building the CNN

# Convolution -> Max Pooling -> Flattening -> Full Connection

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
# 32            : Number of Feature Map
# 3x3           : rowxcol of Feature Map
# (64, 64, 3)   : input_shapre - 64x64 pixel image with 3 columns for RGB
classifier.add(Convolution2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Step 2 - Pooling
# Stride size : 2x2 matrix
# To reduce number of nodes to next steps - reduce size of feature map
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Convolution2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Inputs are ready to feed into Fully Connected Layer
# Step 4 - Full connection or Hidden layer
# units = Number of nodes in hidden layer = 128
classifier.add(Dense(units = 128, activation = 'relu'))
# activation : sigmoid - Binary classification dog or cat
classifier.add(Dense(units = 1, activation = 'sigmoid'))

# Compiling CNN
# loss : binary_crossentropy - Binary outcome
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images
'''
Image augmentation - is a technique that allows us to enrich our dataset or
  training set without adding more images and therefore that allows us to get 
  good performance result with little or no overfitting even with small amout of images
'''
from keras.preprocessing.image import ImageDataGenerator

# rescale - is done to make sure all the pixel values will be in the range of 0 to 1
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

# steps_per_epoch : Number of images in training set - dogs - 4000, cats - 4000
# validation_steps : Number of images in test set : 2000 = 1000(cat) + 1000(dog)
classifier.fit_generator(training_set,
                         steps_per_epoch = (8000/32),
                         epochs = 25,
                         validation_data = test_set,
                         validation_steps = (2000/32))

classifier.save('my_classifier')

# Making new predictions
from keras.preprocessing import image
import numpy as np
import os

def my_predict_fun(path = '', result = {}):
    images = sorted(os.listdir(path))
    for i in images:
        img = image.load_img(path + '/' + i, target_size = (64,64))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis = 0)
        res = classifier.predict(img)
        if (res[0][0] == 1):
            result.update({i: 'dog'})
        else:
            result.update({i: 'cat'})

result = {}
my_predict_fun('dataset/single_prediction/', result)
for img, res in sorted(result.items()):
    print('Prediction for ', img, 'is', res)