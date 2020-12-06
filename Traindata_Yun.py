#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 20:19:19 2020

@author: yunwang
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 22:15:35 2020

@author: yunwang
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder

#def loadData(fileName):
#    data=[]
#    with open(fileName) as txtData:
#        lines= txtData.readline()
#        i = 0
#        for line in lines:
#            lineData= line.strip().split('\t')
#            lineData= re.split('\s+', line.strip())
#            data.append(lineData)
#            i += 1
#    return data

#if __name__=='__main__':
#    fileName= 'data_cleaned.txt'
#    loadData(fileName)

data = pd.read_csv('jobposts1.txt', header = None)

data.columns = ['text', 'title']

def clean_email_text(text):
#    text = text.replace('\n'," ") 
#    text = re.sub(r"-", " ", text) 
#    text = re.sub(r"\d+/\d+/\d+", "", text) 
#    text = re.sub(r"[0-2]?[0-9]:[0-6][0-9]", "", text) 
#    text = re.sub(r"[\w]+@[\.\w]+", "", text)
#    text = re.sub(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", text) 
    text = re.sub('[^a-z]',' ',text.lower())
    text=re.sub('data sci[a-z]+', ' ', text, re.I)
    text=re.sub('data eng[a-z]+', ' ', text, re.I)
    text=re.sub('software eng[a-z]+', ' ', text, re.I)
    pure_text = ''
    for letter in text:
        if letter.isalpha() or letter==' ':
            pure_text += letter
    text = ' '.join(word for word in pure_text.split() if len(word)>1)
    return text

s_text=data["text"]
data['text'] = s_text.apply(lambda s: clean_email_text(s))


#data= pd.read_csv('data_cleaned.txt', delimiter = "\t",header=[0])

    
X = data['text']
y = data['title']
    

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

counter = CountVectorizer()
counter.fit(X_train)

#count the number of times each term appears in a document and transform each doc into a count vector
X_train = counter.transform(X_train)#transform the training data
X_test = counter.transform(X_test)#transform the testing data

en = LabelEncoder()
en.fit(y_train)
y_train = en.transform(y_train)
y_test = en.transform(y_test)
param_grid = {'max_depth': [5,10,15,20,25,30,40,50],
              'max_features': [1,5,10,15,20,30,40],
              'n_estimators':[5,10,15,20,30]}
#clf=tree.DecisionTreeClassifier()
clf= RandomForestClassifier(n_estimators=10)
clf.fit(X_train,y_train)

#clf = GridSearchCV(SVC(kernel='rbf', class_weight='auto'), param_grid)
#clf = clf.fit(x_train, y_train)
predict=clf.predict(X_test)
accuracy=accuracy_score(y_test,predict)
#print("done in %0.3fs" % (time() - t0))
print("Accuracy:")
print(accuracy)

#RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
