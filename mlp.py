from sklearn.neural_network import MLPClassifier
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score


def MLP(fname):
    description, labels = [], []
    with open(fname) as file:
        for line in file:
            text, title = line.strip().split('\t')
            description.append(text.strip())
            labels.append(title.strip())

    trainData, testData, trainLabels, testLabels = train_test_split(description, labels, test_size=0.3)

    counter = CountVectorizer(stop_words=stopwords.words('english'))
    counter.fit(trainData)

    counts_train = counter.transform(trainData)
    counts_test = counter.transform(testData)

    mlp_classifier = MLPClassifier()

    mlp_grid = [ 
        {
            'solver':['lbfgs','adam','sgd'], 
            'hidden_layer_sizes':[(100,),(50,0),(20,20),(50,50),(200,),(400,)], 
            'max_iter':[100, 200, 500, 1000,3000],
        } 
        ]

    gridSearch = GridSearchCV(mlp_classifier, mlp_grid, cv=5)

    gridSearch.fit(counts_train, trainLabels)

    predicted = gridSearch.predict(counts_test)
    print(f'Accuracy = {accuracy_score(predicted, testLabels)}')

if __name__ == "__main__":
    MLP('data_cleaned.txt')