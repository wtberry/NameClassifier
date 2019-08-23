"""
This script will scrape the list of names from
Meiji Yasuda Seimei website's yearly top 100 most popular first name.
between 2004 - 2017

Recording it as Key-Value style database
"""

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
        gender_name.append({"rank":rank, "fname":fname.strip(), "Population":int(pop.strip("人")), "perc":float(perc.strip("%"))})


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
    URL = "https://www.meijiyasuda.co.jp/enjoy/ranking-{}/best100/".format(year)

    soup = load_soup(URL)

    gender_table = soup.find_all("div", {"class":"rankingTableContainer"}) 

    name_dic = {}
    name_dic['male'] = get_gender_name(gender_table[0])
    name_dic['female'] = get_gender_name(gender_table[1])
    return name_dic

year_name = {}
for y in range(2004, 2018):
    # 2004~2017 with this format
    year_name[str(y)] = get_year_name(y)