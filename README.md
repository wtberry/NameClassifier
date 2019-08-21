# Name Classifier Module/Class

This module (class) is a NameClassifier class, and it classifies where a person's name originated from. 
Naive Bayes algorithm is used and impletented with scikit-learn package. 
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
1. edit `region_list.txt` to add or remove the country of your choice, from [Faker documentation](https://faker.readthedocs.io/en/master/)'s locale region codes and country names.
2. generate the data using `create_data.py`, specifying output and country list file name
3. trian, predict, test and visualize using the module from `model.py`

### 2. Pre-trained Model
1. import NameClassifier from model.py
2. use `.load_model(fileName.pickle)` method to load the model`

## Files
- Multi Class Name Classification with Naive Bayes.ipynb
	* goes over how to perform multiclass name classification with NameClassifier class.
- Name Classification with Naive Bayes.ipyn
	* binary classification for Japanese and non-Japanese name
- NameClassifier チュートリアル.ipynb
	* same as above, in Japanese
- model.py
	* the module file for NameClassifier
- prep_data.py
	* practice writing data preprocessing class
- preprocess.py
	* practice data preprocessing
- test.py
	* testing script for module.py
## List of methods and attributes
### Methods
- \__init__https://faker.readthedocs.io/en/master/
    - instantiate the class when training from scratchhttps://faker.readthedocs.io/en/master/.
    
- load_data()
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

- plot_confusion
    - plots the confusion matrix with provided test data
    - param:
        - yt(ndarray): ground truth labels
        - prediction_test(ndarray): predicted labels, integer

- load_model
    - Load the saved model from pickle file
    - Param:
        - file_name(str): the file name of the model you want to load, including the path to the file,
        
- save_model(self, file_name)
    - Saves the class using pickle. 
    - Params:
        - file_name(str): file name including the path to the file and extension(.pickle) 


