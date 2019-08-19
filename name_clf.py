# -*- coding: utf-8 -*-
'''
名前のストリングにアルファベットが２文字以上含まれていれば外国人判定するScript
'''
import string
import sys
name = '高橋　渉'
fname = 'John Smith'


# iter through the name string, to count the numbers of foregin characters


def clf(name, alp_num=2):
    # alp_numの値以上アルファベットが含まれていれば外国人判定

    for_letter = 0
    for l in name:
        if l in string.ascii_letters:
            for_letter+=1

    if for_letter >= alp_num:
        return 'foreign'
    else:
        return 'Japanese'

pipe = sys.stdin
print('name, nationality')
for line in pipe:
    if line.lower() != 'name':
        print("{},{}".format(line.rstrip(), clf(line)))
