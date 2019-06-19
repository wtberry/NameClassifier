
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
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
       
    ### Some utility functions for data preprocess etc
    # load data from csv on pandas, not tied to class
    def load_data(self, file_name, test_size=0.3):
        '''
        - load jp_names, f_names csv as pandas database, add labels,
        - combine japanese & english names
        - separate data for training and test

        @jp_names & f_names:String - full path to the data file, including train & testdataset
        return: x_train, x_test(as pandas series of names), y_train, y_test(as numpy arr of labels)
        '''
        df = pd.read_csv(file_name)
        labels = df['code'].values.reshape(-1, 1)
        self.label_encoder = OrdinalEncoder().fit(labels)
        labels = self.label_encoder.transform(labels)

        return train_test_split(df['name'], labels.ravel(), test_size=test_size, shuffle=True)

    def train(self, X_train, y_train):
        # fit the vectorizer
        print('Fitting the vectorizer and training the model...')
        self.vec = CountVectorizer().fit(X_train)
        self.word_vec = self.vec.transform(X_train)
        # train the ML model
        self.model.fit(self.word_vec, y_train)
        print('training completed!')

    def predict(self, names):
        name_vector = self.vec.transform(names)
        # .predict
        return self.model.predict(name_vector)

    def evaluate(self, names, labels):
        '''
         make prediction, and evaluate the model's
         - accuracy, precision, recall
        '''
        prediction = self.predict(names)
        #TP, FP, TN, FN = self.measure(prediction, labels)
        acc = (prediction == labels).mean()
        # precision
        #precision = TP/(TP + FP)
        # recall
        #recall = TP/(TP + FN)

        return acc
        #return {'accuracy':acc, 'precision':precision, 'recall':recall}

    def get_word_dict(self, corpus=None):
        '''This method returns word frequency dictionary, from the training data
        of the model or given corpus if any.

        Params:
            corpus(list/Series): python list or pandas series of names.This is default to
            None, in which case frequency dictionary is created on the data the model was trained on.

        Returns: 
            dictionary: python dictionary with names as keys, and their frequencies as values.
        '''
        freq_dic = {}
        if corpus is None:
            vector = self.vec
            bag_words = self.word_vec
        else:
            vector = CountVectorizer().fit(corpus)
            bag_words = vector.transform(corpus)

        feature = vector.get_feature_names()
        sum_words = bag_words.sum(axis=0).tolist()[0] # list within list
        
        for i, word in enumerate(feature):
            freq_dic[word] = sum_words[i]

        return freq_dic

    def plot_confusion(self, yt, prediction_test):
        self.cm = confusion_matrix(yt, prediction_test)
        fig = plt.figure(figsize=(10, 8))
        plt.imshow(self.cm, interpolation='nearest')
        plt.colorbar()
        axis_font = {'size': 13, 'color':'black'}
        self.cat = self.label_encoder.categories_[0]
        num_class = len(self.cat)
        classNames = [self.cat[i] for i in range(num_class)]
        plt.title("Confusion Matrix by class", fontdict=axis_font)
        plt.ylabel("True Label", fontdict=axis_font)
        plt.xlabel("Predicted Label", fontdict=axis_font)
        tick_marks = np.arange(len(classNames))
        plt.xticks(tick_marks, classNames, rotation=45)
        plt.yticks(tick_marks, classNames)
        fdic = {'size':10, 'color':'white', 'weight':'heavy'}
        for i in range(num_class):
            for j in range(num_class):
                plt.text(j, i, str(self.cm[i, j]), fontdict=fdic, horizontalalignment='center',verticalalignment='center')
        plt.show()

    '''
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
    '''
        

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


        

