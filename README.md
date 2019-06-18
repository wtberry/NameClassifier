# Name Classifier Module/Class

This module (class) is a NameClassifier class, and it classifies if a person's name string is Japanese or not. It's based on 
Naive Bayes algorithm, impletented with scikit-learn package. 
It's still in a development / prototyping phase, and might have some error / bug.

## Dependencies
This class utilizes libraries, such as
- scikit-learn
- pandas
- pickle

So make sure all of these packages are installed, as well as thier dependencies. 

## How to use??
This class can be imported within a python script, or interpreter.
There are 2 main use cases, 
1. You want  to train the model with your own data, from scratch.
2. You want to load pre-trained model, and deploy it. 

### 1. Train your own

### 2. Pre-trained Model

## List of methods and attributes

### Methods
- \__init__
    - instantiate the class when training from scratch.
    
- load_data() (static)
    - given file names, load the data as pandas Dataframe, add column for label, and split the data into train and test set.
        - params:
            - jp_names(str): file name and full path to csv, containing Japanese names.
            - f_names(str): file name and full path to csv, containing non-Japanese names
        - returns: x_train, x_test, y_train, y_test
            - pandas Series: 2 Series, each containing training & test name data
            - ndarray: 2 ndarray, each containing training and test labels. 
- train
    - given training data, vectorize the data and train the Naive Bayes classifier.
    - params:
        - X_train(pandas Series): containing name strings for training.
        - y_train(ndarray): containing labels, 1s and 0s for training.
    
- predict
    - given names' data, predict whether the names are Japanese or not
    - params:
        - names(list/pandas Series): containing strings of names
    - returns:
        - list: list of 1s and 0s, 1 for Japanese and 0 for non-Japanese.

- evaluate
    - evaluate the model with given test data
    - param:
        - names(list/ndarray): of name strings of people
        - labels(ndarray): of name strings, label
    - returns: 
        - dictionary: dictionary of model accuray, precision and recall.
- measure (static)
    - utility methods for in-class use, calclate True&Flase Positive&Negative
    - param:
        - pred(list/ndarray): predicted values
        - label(ndarray): label/ground truth
- load_model
    - Load the saved model from pickle file
    - Param:
        - file_name(str): the file name of the model you want to load, including the path to the file,
- save_model(self, file_name)
    - Saves the class using pickle. 
    - Params:
        - file_name(str): file name including the path to the file and extension(.pickle) 

