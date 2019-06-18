from model import NameClassifier
import pandas as pd

## Load the pre-trained model and test it
clf = NameClassifier.load_model('model/first_clf.pickle')

x_train, x_test, y_train, y_test = NameClassifier.load_data('data/jp_names.csv', 'data/f_names.csv')
jp_sample = pd.read_html('data/fake_j_name.html')[0]
jp_names = jp_sample['名前']

