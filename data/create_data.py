'''
This script creates fake name data for
- Japanese name
- non_japanese
with Faker library
'''
from faker import Faker
import pandas as pd

def create_jp_name(num=100):

    fake = Faker('jp_JP')
    
    f = open('jp_names.csv', "w")
    f.write('code,name\n')
    for _ in range(num):
        name = fake.name()
        f.write("{},{}\n".format('jp_JP', name))
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
        else:
            for _ in range(num):
                name = fake.name()
                f.write("{},{}\n".format(country, name))

    f.close()
