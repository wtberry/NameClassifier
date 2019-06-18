'''
このスクリプトはPandasライブラリでデータファイルを読み込み、
SKlearnか使えるデータに加工する
データはこのスクリプトのあるフォルダ内のdata/ というフォルダにCSV形式で
保存してください。
実行する際は実際のCSVファイル名に変更する。
'''
import pandas as pd 
import os 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# このPythonファイルがあるフォルダのパス
PATH = os.path.dirname(os.path.realpath(__file__))
PATH = os.path.join(PATH, 'data')
print(PATH)
# 日本、外国人の名前のファイル名
jp_fname = "jp_names.csv"
f_fname = "f_names.csv"

# データを読み込む
jp = pd.read_csv(os.path.join(PATH, jp_fname))
fr = pd.read_csv(os.path.join(PATH, f_fname))

jp['name'] = jp['name'].astype(str)
fr['name'] = fr['name'].astype(str)

# ラベルを追加
jp['label'] = int(1)
fr['label'] = int(0)

data = pd.concat([jp, fr], axis=0)

# データを作る
# SklearnのCountVectorizerを利用し、単語（姓、名）の頻度に基づきベクトル化
vectorizer = CountVectorizer()
name_vec = vectorizer.fit_transform(data['name'])
y = data['label'].values
print('shape of the vectorized data is: ', name_vec.shape)

# トレイニングとテスト用データに分ける
X_train, X_test, y_train, y_test = train_test_split(name_vec, y, shuffle=True)
