'''
This script creates fake name data for
- Japanese name
- non_japanese
with Faker library

USE THIS IN CONDA's BASE environment
'''
from faker import Faker
import pandas as pd

def create_jp_name(num=100, fileName='jp_names.csv', mix_char=False):
    '''
    generate fake japanse name.
    Param:
        num: numbers of names to generate
        fileName: filename to save the result on
        mix_char: Generate Kanji, Katakana and Roman letter repsetented names if True. Kanji Only otherwise
    '''

    fake = Faker('jp_JP')
    
    f = open(fileName, "w")
    f.write('code,name\n')

    if mix_char == False:
        for _ in range(num):
            name = fake.name()
            f.write("{},{}\n".format('jp_JP', name))
    elif mix_char == True:
        for _ in range(int(num/3)):
            name = fake.name()
            f.write("{},{}\n".format('jp_JP', name))
            romanized_name = ' '.join(fake.romanized_name().split(' ')[::-1])
            f.write("{},{}\n".format('jp_JP', romanized_name))
            kata_name = fake.kana_name()
            f.write("{},{}\n".format('jp_JP', kata_name))
            print('.', end='')

    f.close()



def create_foreign_name(loc='None', num=100, country_list='region_list.txt', fileName='f_names.csv'):
    '''
    create fake names with 
    - loc: location(str, location code)
    - num: how many names/country?
    '''
    #fake = Faker(loc)

    #for _ in range(num):
    #    name = fake.name()
    #    print(name)
        

    # read in the list of countries
    l = pd.read_csv(country_list)
    f = open(fileName, "w")
    f.write('code,name\n') # first line, col name

    # now make data for each country, and write in the file
    for i in range(len(l)):
        row = l.iloc[i]
        code, country = row['code'], row['country']
        print("making name for ", code)
        fake = Faker(code)
        if code == 'zh_CN' or code == 'zh_TW' or code == 'ko_KR':
            for _ in range(num):
                name = fake.name()
                f.write("{},{} {}\n".format(country, name[0], name[1:]))
            if _%100 == 0:
                print('.', end='')
        else:
            for _ in range(num):
                name = fake.name()
                f.write("{},{}\n".format(country, name))

    f.close()
