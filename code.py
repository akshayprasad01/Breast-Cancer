#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 23:20:50 2019

@author: Akshayprasad Arunkumar
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

Data_dir = "/Users/administrator/Desktop/Dataset_1"

Categories = ["Malignant","Benign"]
# paths to Malignant or benign  
'''for i in Categories:
    path = os.path.join(Data_dir,i)
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path,img))
        #plt.imshow(img_array)
        #plt.show()
'''

training_data = []

def create_training_data():
    for i in Categories:
        path = os.path.join(Data_dir,i)
        class_num = Categories.index(i)
        for img in os.listdir(path):
            img_array = cv2.imread(os.path.join(path,img),0)            
            ret,img_array = cv2.threshold(img_array,240,255,cv2.THRESH_BINARY)
            img_array = np.array(img_array)
            #img_array = cv2.resize(img_array, (256,256),interpolation = cv2.INTER_AREA)
            lol = img_array.shape
            #plt.imshow(img_array)
            if lol == (50,50):
                print(lol)
                img_array = img_array.reshape(len(img_array),-1)
                #new_array = cv2.resize(img_array,(2048,6144))
                #plt.imshow(img_array)
                #plt.show()
                # append the data to te list and get ready
                training_data.append([img_array,class_num])
           
create_training_data()

#print(training_data)
import random

random.shuffle(training_data)

X_train = []
Y_train = []

for features,label in training_data:
    X_train.append(features)
    Y_train.append(label)

X_train = np.array(X_train)
X_train = X_train.reshape(len(X_train),-1)



from sklearn.preprocessing import LabelEncoder
lab_enco=LabelEncoder()

Y_train = lab_enco.fit_transform(Y_train)
print(lab_enco.classes_)

# one hot encoding for the output
from keras.utils.np_utils import to_categorical as tc
Y_train = tc(Y_train)


'''Data_dir_1 = "C:/Users/moopa/Desktop/Dataset/test"

testing_data = []

def create_testing_data():
    for i in Categories:
        path = os.path.join(Data_dir_1,i)
        class_num = Categories.index(i)
        for img in os.listdir(path):
            img_array = cv2.imread(os.path.join(path,img),cv2.IMREAD_GRAYSCALE)
            img_array = np.array(img_array)
            lol = img_array.shape
            if lol == (2048,2048):
                img_array = img_array.reshape(len(img_array),-1)
                #new_array = cv2.resize(img_array,(2048,6144))
                #plt.imshow(img_array)
                #plt.show()
                # append the data to te list and get ready
                testing_data.append([img_array,class_num])
           
create_testing_data()

X_test = []
Y_test = []

for features,label in testing_data:
    X_test.append(features)
    Y_test.append(label)

X_test = np.array(X_test)
X_test = X_test.reshape(len(X_test),-1)

Y_test = lab_enco.fit_transform(Y_test)
print(lab_enco.classes_)'''

from sklearn.model_selection import train_test_split as tss

X_train,X_test,Y_train,Y_test = tss(X_train,Y_train,test_size = 0.3,random_state = 0)
X_train,X_val,Y_train,Y_val = tss(X_train,Y_train,test_size = 0.1,random_state = 0)

from keras.models import Sequential
from keras.layers import Dense

cancer_classifier = Sequential()
cancer_classifier.add(Dense(512,input_dim = len(X_train[0]),activation = 'relu'))
cancer_classifier.add(Dense(512,activation = 'relu'))
cancer_classifier.add(Dense(512,activation = 'relu'))
cancer_classifier.add(Dense(512,activation = 'relu'))
cancer_classifier.add(Dense(len(Y_train[0]),activation = 'softmax'))

cancer_classifier.compile(optimizer = 'adam',loss = 'categorical_crossentropy',metrics = ['accuracy'])

classifier = cancer_classifier.fit(X_train,Y_train,batch_size = 30,epochs = 10,validation_data = (X_val,Y_val),verbose = 1)

accuracy = cancer_classifier.evaluate(X_test,Y_test,verbose = 1)

print("Accuracy: {0}".format(accuracy[1]*100))
ssup = cancer_classifier.predict(X_test)
for i in ssup:
    if i[0]>i[1]:
        i[0] = 1
        i[1] = 0
    else:
        i[1] = 1
        i[0] = 0
from sklearn.metrics import accuracy_score

accu = accuracy_score(ssup,Y_test)
print(accu)
    

