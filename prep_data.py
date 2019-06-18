'''
このクラスでは名前のCSVファイルを読み込み、CountVectorizerで
BagOfWordsを用いて名前データをベクトル化し、機械学習モデルが
使えるように加工する。
必要なパッケージは：
- os
- pandas
- numpy
- scikit learn
'''
import os 
import pickle
import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split


class nameToVector(object):

    def __init__(self):
        # このPythonファイルがあるフォルダのパス
        self.cur_PATH = os.path.dirname(os.path.realpath(__file__))
        self.PATH = os.path.join(self.cur_PATH, 'data')
        print(self.PATH)

    def load_data(self, japanese_name, foreign_name):

        # 日本、外国人の名前のファイル名
        jp_fname = japanese_name
        f_fname = foreign_name

        # データを読み込む
        jp = pd.read_csv(os.path.join(self.PATH, jp_fname))
        fr = pd.read_csv(os.path.join(self.PATH, f_fname))

        # ラベルを追加
        jp['label'] = int(1)
        fr['label'] = int(0)
        
        self.data = pd.concat([jp, fr], axis=0)


    def get_name_vector(self):
        # 読んだCSVをベクトル化, Vectorizerも保つ
        # SklearnのCountVectorizerを利用し、単語（姓、名）の頻度に基づきベクトル化
        vectorizer = CountVectorizer()
        self.name_vec = vectorizer.fit_transform(self.data['name'])
        self.y = self.data['label'].values
        print('shape of the vectorized data is: ', self.name_vec.shape)

    def load_name_vector(self, file_name):
        # 保存されているCountVectorを読み込む??
        self.name_vec = pickle.load(open(os.path.join(self.cur_PATH, file_name), 'rb'))
        


    def transform(self, name):
        # 新しい名前をStringでうけとり、ベクトル化
        # name: 名前のStringを含むPandasのSeriesかPythonリスト
        return self.name_vec.transform(name)



