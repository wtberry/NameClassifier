'''
このファイルではSklearnを用いてベイズ分類器を実装。
preprocessで読み込んだデータを元にモデルをトレイニングし、テストする。
'''
from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB()
clf.fit()