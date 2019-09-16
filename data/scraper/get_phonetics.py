"""
This script reads in the list of first names in kanji, and 
look up their phonetic letters in hiragana, as well as sex

- URL: https://b-name.jp/赤ちゃん名前辞典
- if not found on the above, then fall back to..
- URL2: https://kanji.reader.bz/
- URL3: http://name.m3q.jp/list?g=&s={}
- when collected, it'll save it in a dictionary with key of the name, and 
value as [] of phonetics.
"""
import os
import csv
import sys
import glob
import re
import requests
from bs4 import BeautifulSoup as bs


def load_soup(URL):
        '''
        Given URL, access the page and get the soup obj
        Args:
            URL:string of URL of the word on the dictionary
        Reutrn:
            BeautifulSoup object
        '''
        # get soup from URL
        try:
            r = requests.get(URL)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as cerr:
            print(cerr)
            #sys.exit("Check your internet connection?")
            return None
        except requests.exceptions.HTTPError as httpErr:
            print(httpErr)
            #sys.exit("wrong word")
            return None
        except requests.exceptions.Timeout as to:
            print(to)
            return None
            #sys.exit("connection timed out")
        except requests.exceptions.TooManyRedirects as tmr:
            print(tmr)
            return None
            #sys.exit("too many redirection. tor?")
        except requests.exceptions.RequestException as e:
            #sys.exit("soething went wrong")
            print(e)
            return None

        return bs(r.content, 'lxml')


def Jinmei_dict(idx, name):
    URL_alt_tmp = "https://kanji.reader.bz/{}"
    URL_alt = URL_alt_tmp.format(name)

    soup = load_soup(URL_alt)

    if soup == None:
        return [[idx, name, "Error", "UNK"]]

    else:
        # phonetics in the first p tag
        try:
            first_p = soup.find_all('p')[1]
        except IndexError as ie:
            print("Weird index error")
            return None

        name_text = first_p.text.replace("、", " ").split(" ")

        if "見つかりませんでした。" in name_text[0]:
            print("{} was not found on Jinmei dict".format(name))
            return None
        else:
            # extract hiragana 
            hiragana = "[\u3040-\u309F]+"
            prog = re.compile(hiragana)
            gender = "UNK"
            result = [] 
            for phonetic in name_text:
                if prog.match(phonetic):
                    #print([idx, name, phonetic, gender])
                    result.append([idx, name, phonetic, gender])

            return result



def Baby_name(idx, name):
    """
    Go to the baby name website, look for the phonetics of the given name in kanji,
    return the list of list of name, phonetic and sex.
    If not found, return None.
    """
    URL_temp = "https://b-name.jp/赤ちゃん名前辞典/?q={}&mode=2&sex=all"
    URL = URL_temp.format(name)
    print("Getting phonetics for {} at baby name website...".format(name))
    soup = load_soup(URL)

    if soup == None:
        return [[idx, name, "Error", "UNK"]]

    else:
        # check if the name exist on the website
        not_found = "お探しのお名前は見つかりませんでした。"
        try:
            p_tag = soup.find_all('p')[2]
        except IndexError as ie:
            print("Weird index out of range error")
            return None
        if not_found in p_tag.text:
            print("{} was not found on Baby name web...".format(name))
            return None
        else:
            # keep collecting phonetics
            # tables of 3 in the page, but the first table contains the name and gender
            name_table = soup.find_all("table")[0]
            rows = name_table.find_all('tr')[1:]
            result = []
            # iter through the each phonetics
            for row in rows:
                # get the gender first
                gender = row.find("td").get("class")[0][5:]
                textList = row.text.split("\n")
                kanji = textList[2]
                phonetic = textList[3]
                #print([idx, name, phonetic, gender])
                result.append([idx, name, phonetic, gender])

            return result

### THis part is no longer developed
"""
def baby_name_two(idx, name):

    #GO to the last resort, bname website, and get the name
    #If not found, return empty

    URL_temp = "http://name.m3q.jp/list?g=&s={}"
    URL = URL_temp.format(name)
    print("Getting phonetics for {} at baby name 2...".format(name))
    soup = load_soup(URL)

    if soup == None:
        return [[idx, name, "Error", "UNK"]]

    else:
        # check if the name exist on the website
        not_found = "見つかりませんでした"
        h4 = soup.find('h4')
        if not_found in h4.text:
            print("{} was not found on Baby name web...".format(name))
            return None

        else:
            # get the name table
            name_table = soup.select('tr[class*="no-"]')
            # iterate it and get the info
            result = {'index':[], 'first_name':[], 'hira':[], 'gender':[], 'roman':[], 'kata':[]}
            for row in name_table:
                gender = row.find('i').get("class")[0][5:]
                kanji = row.text.split("\n")[8]
                phonetic = row.text.split("\n")[5]
                #result.append([idx, name, phonetic, gender])
                result['index'].append(idx)
                result['first_name'].append(name)
                result['hira'].append(phonetic)
                result['gender'].append(gender)
                result['roman'].append("NF")
                result['kata'].append("NF")


            return result

"""

def record_row(result, writer):
    """
    Given the writer ojb and list of the list of idx, name, phonetic, and gender,
    write it on csv and dictionary
    And return the mini dictionary
    And print each row
    """
    name_dic = {'man':[], 'woman':[], 'UNK':[]} # dict with one names' info
    for row in result:
        writer.writerow(row)
        name_dic[row[3]].append(row[2])
        print(row)
    return name_dic




f = open("first_name_list.csv", "r")
name_list = [line.strip('\n') for line in f]
total = len(name_list)
#name_list = ['渉', '青豆', 'ウルトラマン']

# recordindg devices
names_dic = {}

out = open("f_name_phonetics1.csv", 'a')
#out = open("test_name_phonetics.csv", 'a')
writer = csv.writer(out)

# iter through the name list, and pull the phonetics and gender for each name
for idx, name in enumerate(name_list):
    print("{}/{} th, {}".format(idx, total, name))
    bname = Baby_name(idx, name)
    if bname:
        # if the name was found, record it
        record_row(bname, writer)
    else:
        print("{} not found in the first dictionary, searching on the 人名辞典...".format(name))
        jinmei = Jinmei_dict(idx, name)
        # see if it has a result
        if jinmei:
            # record it
            record_row(jinmei, writer)
        else:
            print("{} wasn't found on 人名辞典... using the python module to convert".format(name))
            # just record as not found, NF
            result = [[idx, name, "NF", "UNK"]]
            record_row(result, writer)



out.close()