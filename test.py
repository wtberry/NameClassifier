from model import NameClassifier
import pandas as pd

# インスタンスをclfとして作成
clf = NameClassifier()

# このメソッドは x_train, x_test, y_train, y_test をこの順番で返します。
x_train, x_test, y_train, y_test = clf.load_data(['data/jp_names.csv', 'data/f_names.csv'], test_size=0.4)

print('名前データ　 type:{}\n{}'.format(type(x_train), x_train.sample(10)))
print('\nラベル: 　{}, type: {}'.format(y_train, type(y_train)))

# 学習データを入力し、学習させる。
clf.train(x_train, y_train)

# モデル評価、３つの値を含んだディクショナリを返す。
model_eval = clf.evaluate(x_test, y_test)
st = '正解率：{}%\n適合率：{}\n再現率：{}'.format(model_eval['accuracy']*100, model_eval['precision'], model_eval['recall'])
print(st)

saved_model = 'trained_model.pickle'
# モデルを保存、ファイルパス、ファイル名、拡張子を忘れずに。
#clf.save_model('model/'+ saved_model)
#print('{} was successfully saved!'.format(saved_model))

input("wanna load the saved model and test it?? hit any bottob")

# モデルを読み込む。
#trained_clf = NameClassifier.load_model('model/trained_model.pickle')
# モデルを評価
#model_eval = trained_clf.evaluate(x_test, y_test)
#st = '正解率：{}%\n適合率：{}\n再現率：{}'.format(model_eval['accuracy']*100, model_eval['precision'], model_eval['recall'])
#print(st)

# 他の名前で予測してみる
names = ['John Wick', '문　재인', '佐藤　たける']
print(clf.predict(names))
