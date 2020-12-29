import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

pd.set_option('display.max_columns', None)
data = pd.read_csv('data_banknote_authentication.csv')


X = data[['variance','skewness','curtosis','entropy']].values
Y = data[['class']].values

X_train ,X_test , Y_train , Y_test = train_test_split (X,Y, test_size =0.5 ,random_state =0)


accuracy_list = []
for i in [3,5,7,9,11]:
    accuracy = 0
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    X_train ,X_test , Y_train , Y_test = train_test_split (X,Y, test_size =0.5 ,random_state =30)
    knn_classifier = KNeighborsClassifier (n_neighbors =i)
    knn_classifier.fit (X_train,Y_train.ravel())
    prediction = knn_classifier.predict(X_test)
    correct = 0
    for j in range(len(prediction)):
        if prediction[j] == 0 and Y_test[j][0] == 0:
            TP+=1
        elif prediction[j] == 0 and Y_test[j][0] == 1:
            FP+=1
        elif prediction[j] == 1 and Y_test[j][0] == 1:
            TN+=1
        elif prediction[j] == 1 and Y_test[j][0] == 0:
            FN+=1
    accuracy = (TP+TN)/len(prediction)
    accuracy_list.append(accuracy)
    print('k = %d,accuracy = %f'%(i,accuracy))