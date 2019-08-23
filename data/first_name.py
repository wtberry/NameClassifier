"""
This script will scrape the list of names from
Meiji Yasuda Seimei website's yearly top 100 most popular first name.
between 2004 - 2017

Recording it as Key-Value style database
"""
import json
import requests
from bs4 import BeautifulSoup as bs
import csv
import sys

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
            sys.exit("Check your internet connection?")
        except requests.exceptions.HTTPError as httpErr:
            print(httpErr)
            sys.exit("wrong word")
        except requests.exceptions.Timeout:
            sys.exit("connection timed out")
        except requests.exceptions.TooManyRedirects:
            sys.exit("too many redirection. tor?")
        except requests.exceptions.RequestException as e:
            sys.exit("soething went wrong")

        return bs(r.content, 'lxml')


#rank_count = 0

def get_names(rows):
    """input is a collection of rows in one table"""

    # Design
    """ executing if - else for index within the loop does not slow down the parsing too much"""
    for row in rows:
        row=row.find_all("td")

        global rank_count #why is this global thing working?
        rank_count += 1
        if len(row)==5:
            rank, fname, pop, perc = rank_count, row[2].text, row[3].text, row[4].text
        elif len(row)==4:
            rank, fname, pop, perc = rank_count, row[1].text, row[2].text, row[3].text
        else:
            print("invalid name table size, check the website at: ", URL)
            sys.exit()
        
        global gender_name
        # checkin the data if it's valid
        try:
            pop = int(pop.strip("人"))
        except:
            pop = None

        # checkin the data if it's valid
        try:
            perc = float(perc.strip("%"))
        except:
            perc = None
        gender_name.append({"rank":rank, "fname":fname.strip(), "Population":pop, "perc":perc})


#rows = tables[0].find_all('tr')
def get_gender_name(gender):
    """
    provided with gender_table (guy / girl's name), will return / print 
    names in the table
    """
    global rank_count # Why is this global within function working now?
    rank_count = 0
    global gender_name
    gender_name = [] # list to store each gender's name dic
    tables = gender.find_all("tbody")
    for rows in tables:
        get_names(rows.find_all('tr'))
    return gender_name


def get_year_name(year):
    """get year from 2004 - 2011"""
    URL = "https://www.meijiyasuda.co.jp/enjoy/ranking-{}/best100/".format(year)

    soup = load_soup(URL)

    gender_table = soup.find_all("div", {"class":"rankingTableContainer"}) 

    name_dic = {}
    name_dic['male'] = get_gender_name(gender_table[0])
    name_dic['female'] = get_gender_name(gender_table[1])
    return name_dic, URL

def get_name_from_list(URL):
    """For 2012 - 2017, provided with name's list, iter though and put in dictionary"""
    soup = load_soup(URL)
    table_list = soup.find_all('table')[0].text.split('\n\n\n\n')[1:]
    name_list = [row.split('\n') for row in table_list] # split at new line, 2D list
    # iter through each row and put info in the dic
    count = 0
    gender_name = []
    for row in name_list:
        if len(row) == 4:
            rank, fname, pop, perc = count, row[1], row[2], row[3]
             # checkin the data if it's valid
            try:
                pop = int(pop.strip("人"))
            except:
                pop = None
            # checkin the data if it's valid
            try:
                perc = float(perc.strip("%"))
            except:
                perc = None

            gender_name.append({"rank":rank, "fname":fname.strip(), "Population":pop, "perc":perc})
        
    # put the list in the dictionary
    return gender_name

def get_year_name_later(year):
    """get year from 2012 - 2017""" 
    print(year)
    result = {}
    genders = ['boy', 'girl']
    for gender in genders:
        URL = "https://www.meijiyasuda.co.jp/enjoy/ranking-{}/best100/{}.html".format(year, gender)
        result[gender] = get_name_from_list(URL)
    return result, URL

        
    


    #gender_table = soup.find_all("div", {"class":"rankingTableContainer"}) 
    #name_dic = {}
    #print("geder table length: ", len(gender_table))
    #name_dic['male'] = get_gender_name(gender_table[0])
    #name_dic['female'] = get_gender_name(gender_table[1])
    #return name_dic, URL



year_name = {}
for y in range(2004, 2018):
    if y < 2012:
        # 2004 - 2011
        year_name[str(y)], URL = get_year_name(y)
    else:
        # then they changed format kindly, for 2012 - 2017
        year_name[str(y)], URL = get_year_name_later(y)
    
    print(y, "done")

# newest year, assuming as 2018
genders = ['boy', 'girl']
result = {}
for gender in genders:
    URL = "https://www.meijiyasuda.co.jp/enjoy/ranking/best100/{}.html".format(gender)
    result[gender] = get_name_from_list(URL)
year_name['2018'] = result

# now write to json
with open("first_name.json", "w", encoding='utf8') as fp:
    json.dump(year_name, fp)

# 2004 ~ 2011 in the original

# 2012 ~ 2017 in secondary

# 2018??