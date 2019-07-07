from model import NameClassifier
import pandas as pd

## Load the pre-trained model and test it
clf = NameClassifier()

x_train, x_test, y_train, y_test = clf.load_data('data/multi_class.csv')
clf.train(x_train, y_train)
print('acc: ', clf.evaluate(x_test, y_test))
pred = clf.predict(x_test)
clf.plot_confusion(y_test, pred)
