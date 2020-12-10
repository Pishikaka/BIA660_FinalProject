"""
A simple script that demonstrates how we classify textual data with sklearn.

"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from sklearn.svm import SVC
import pandas as pd
import re
import csv

data = pd.read_csv('jobposts(1).txt', header = None)

data.columns = ['text', 'title']

def predjob(filenm,VT,counter):
    fw = open('predictions.txt','w',encoding = 'utf-8')
    testdt = []
    writer = csv.writer(fw, lineterminator = '\n')

    with open(filenm) as file:
        testdt = list(file.readline())
    counts_test = counter.transform(testdt)
    for x in counts_test:
        predout = VT.predict(x)
        writer.writerow([predout])
    fw.close()
            
def clean_email_text(text):
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

def vt():
    #read the reviews and their polarities from a given file
    s_text=data["text"]
    data['text'] = s_text.apply(lambda s: clean_email_text(s))
    
    
    #data= pd.read_csv('data_cleaned.txt', delimiter = "\t",header=[0])
    
    
    description = data['text'].values
    labels = data['title'].values
    
    trainData, testData, trainLabels, testLabels = train_test_split(description, labels, test_size=0.3)
    
    counter = CountVectorizer(stop_words=stopwords.words('english'))
    counter.fit(trainData)
    
    counts_train = counter.transform(trainData)
    counts_test = counter.transform(testData)
    
    
    
    '''
    #Build a counter based on the training dataset
    counter = CountVectorizer()
    counter.fit(rev_train)
    
    
    #count the number of times each term appears in a document and transform each doc into a count vector
    counts_train = counter.transform(rev_train)#transform the training data
    counts_test = counter.transform(rev_test)#transform the testing data
    '''
    
    #train classifier
    model1 = RandomForestClassifier(max_depth = 40, max_features = 60, n_estimators =50)
    model2 = KNeighborsClassifier(n_neighbors = 40, weights='distance')
    model3 = LogisticRegression(solver='liblinear',C = 0.5, max_iter = 100, penalty = 'l2')
    model4 = MLPClassifier(solver='lbfgs',hidden_layer_sizes=(20,20),max_iter = 3000)
    model5 = SVC(C = 5.0, kernel='rbf', degree=10, cache_size=200)
    predictors=[('dt',model1),('nb',model2),('lreg',model3),('MLP',model4),('sv',model5)]
    
    VT=VotingClassifier(predictors)
    
    #train all classifier on the same datasets
    VT.fit(counts_train,trainLabels)
    
    #use hard voting to predict (majority voting)
    pred=VT.predict(counts_test)
    
    #print accuracy
    print (accuracy_score(pred,testLabels))
    
    
    filenm = 'jobposts.txt'
    predjob(filenm,VT,counter)
    
    

if __name__ == '__main__':
    
    vt()
    