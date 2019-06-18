
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

class NameClassifier(object):
    '''
    ML algorithm to classify names' nationality

    this class is name classifier model class, with 2 attr
    - Vectorizer: to vectorize the data for prediction
    - model: clf for decision making
    Also comes with methods like...
    - saveModel()
    - loadModel()
    - trainModel()
    - predict()
    - evaluate()

    When loading the pre-trained model from pickle file, use the classmethod load like
    trained_model = name_classifier.load_model(file_name)

    Model should be saved at /model
    If any additional methods needed, contact@ wtberry on github
    '''

    def __init__(self):
        # declaire the model variables, classifier (clf) and vectorizer, if training new one
        self.model = MultinomialNB()
        self.vectorizer = CountVectorizer()
    
    ### Some utility functions for data preprocess etc
    # load data from csv on pandas, not tied to class
    @staticmethod
    def load_data(jp_names, f_names, test_size=0.3):
        '''
        - load jp_names, f_names csv as pandas database, add labels,
        - combine japanese & english names
        - separate data for training and test

        @jp_names & f_names:String - full path to the data file, including train & testdataset
        return: x_train, x_test(as pandas series of names), y_train, y_test(as numpy arr of labels)
        '''
        # データを読み込みラベルを追加
        jp = pd.read_csv(jp_names)
        fr = pd.read_csv(f_names)
        jp['label'] = int(1)
        fr['label'] = int(0)
        data = pd.concat([jp, fr], axis=0)

        return train_test_split(data['name'], data['label'].values, test_size=test_size, shuffle=True)

    def train(self, X_train, y_train):
        # fit the vectorizer
        X_train = self.vectorizer.fit_transform(X_train)
        # train the ML model
        print('training the model....')
        self.model.fit(X_train, y_train)
        print('training completed!')

    def predict(self, names):
        name_vector = self.vectorizer.transform(names)
        # .predict
        print('returning list')
        return self.model.predict(name_vector).tolist()

    def evaluate(self, names, labels):
        '''
         make prediction, and evaluate the model's
         - accuracy, precision, recall
        '''
        prediction = self.predict(names)
        TP, FP, TN, FN = self.measure(prediction, labels)
        acc = (prediction == labels).mean()
        # precision
        precision = TP/(TP + FP)
        # recall
        recall = TP/(TP + FN)

        return {'accuracy':acc, 'precision':precision, 'recall':recall}

    @staticmethod
    def measure(pred, label):
        # Calculate TP, FP, TN, FN for precision and recall
        TP, FP, TN, FN = 0,0,0,0 
        for i in range(len(pred)): 
            if pred[i] == label[i] == 1: 
                TP +=1 
            if pred[i] ==1 and label[i]==0: 
                FP +=1 
            if pred[i] == label[i] == 0: 
                TN +=1 
            if pred[i] == 0 and label[i] ==1: 
                FN +=1 
        return TP, FP, TN, FN 
        

    @classmethod
    def load_model(cls, file_name): # instance / class method??
        # https://stackoverflow.com/questions/2709800/how-to-pickle-yourself
        # loading pickled saved model
        # loading itself from the pickle?? lol
        print('loading the model')
        return pickle.load(open(file_name, 'rb'))
    
    def save_model(self, file_name):
        # save this class itself as pickle??
        pickle.dump(self, open(file_name, 'wb'))


        

