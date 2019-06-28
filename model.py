
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
    this class is NameClassifier model class

    Attributes:
        Vectorizer: to vectorize the data for prediction, CountVectorizer
        model: classifier for decision making, based on Naive Bayes

    Methods:
        load_data
        train
        evaluate
        predict
        get_word_dict
        get_label_str
        plot_confusion
        saveModel
        loadModel
    '''

    def __init__(self):
        # declaire the model variables, classifier (clf) and vectorizer, if training new one
        self.model = MultinomialNB()
       
    ### Some utility functions for data preprocess etc
    # load data from csv on pandas, not tied to class
    def load_data(self, file_name, test_size=0.3):
        '''Load the data, encode the labels, and split into train and test set.
        
        Params:
            file_name(string): file path & name to the csv file
            test_size(float): ratio of testing set, between 0 & 1

        Return: x_train, x_test(as pandas series of names), y_train, y_test(as numpy arr of labels)
            These elements will be returned on the order above.
            Pandas Series: name data, X_train and X_test
            ndarray: encoded labels, y_train and y_test
        '''

        df = pd.read_csv(file_name)
        labels = df['code'].values.reshape(-1, 1)
        self.label_encoder = OrdinalEncoder().fit(labels)
        labels = self.label_encoder.transform(labels)

        return train_test_split(df['name'], labels.ravel(), test_size=test_size, shuffle=True)

    def train(self, X_train, y_train):
        '''given training data, this method will fit the vectorizer(bag of words) and train the naive bayes model.
        
        Param:
            X_train(Pandas Series): training name dataset
            y_train(ndarray): training labels dataset
        '''

        # fit the vectorizer
        print('Fitting the vectorizer and training the model...')
        self.vec = CountVectorizer().fit(X_train)
        self.word_vec = self.vec.transform(X_train)
        # train the ML model
        self.model.fit(self.word_vec, y_train)
        print('training completed!')

    def predict(self, names, label_str=False):
        '''Predict name's origin based on the test data. Returns encoded label by default,
        but returns label strings when label_str=True
        
        Param:
            names(ndarray/Pandas Series/list): containing names
            label_str(bool): default False, to return label integers, set it to True to return label strings

        Return:
            array: containing label integers or strings.
        '''

        name_vector = self.vec.transform(names)
        pred = self.model.predict(name_vector)
        if not label_str:
            return pred
        else:
            return self.label_encoder.inverse_transform(pred.reshape(-1,1)).ravel()

    def evaluate(self, names, labels):
        '''make prediction, and evaluate the model's accuracy

        Params:
            names(list/Pandas Series/ndarray): names data
            labels(ndarray): ground truth
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

    def get_label_str(self, labels):
        '''accepts numerically encoded labels and returns corresponding label strings
            param:
                labels(ndarray): ndarray containing numerical labels
            returns:
                ndarray: containing label strings
        '''
        return self.label_encoder.inverse_transform(labels.reshape(-1, 1)).ravel()

    def plot_confusion(self, yt, prediction_test):
        '''Plot confusion matrix, based on given labels and prediction

        Param:
            yt(ndarray): array of gruond truth labels
            prediction_test(ndarray): predicted labels
        '''

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

    @classmethod
    def load_model(cls, file_name): # instance / class method??
        '''Load saved model obj for use.

        Param:
            file_name(string): path to the model file(pickle).
        
        Return:
            NameClassifier: the loaded class obj for use.
        '''
        # https://stackoverflow.com/questions/2709800/how-to-pickle-yourself
        # loading pickled saved model
        # loading itself from the pickle?? lol
        print('loading the model')
        return pickle.load(open(file_name, 'rb'))
    
    def save_model(self, file_name):
        '''Save a trained model obj for future use.

        Param:
            file_name(string): path to the model file(pickle).
        '''
        # save this class itself as pickle??
        pickle.dump(self, open(file_name, 'wb'))
