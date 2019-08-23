"""
This script will scrape the list of names from
Meiji Yasuda Seimei website's yearly top 100 most popular first name.
between 2004 - 2017
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


def get_names(rows):
    """input is a collection of rows in one table"""

    # Design
    """ executing if - else for index within the loop does not slow down the parsing too much"""
    for row in rows:
        row=row.find_all("td")
        if len(row)==5:
            rank, fname, pop, perc = row[0].text, row[2].text, row[3].text, row[4].text
            print(rank, fname, pop, perc)
        elif len(row)==4:
            rank, fname, pop, perc = row[0].text, row[1].text, row[2].text, row[3].text
            print(rank, fname, pop, perc)
        else:
            print("invalid name table size, check the website at: ", URL)
            sys.exit()

year = 2004 # 2004~2017 with this format
URL = "https://www.meijiyasuda.co.jp/enjoy/ranking-{}/best100/".format(year)

soup = load_soup(URL)

gender_table = soup.find_all("div", {"class":"rankingTableContainer"}) 
guy = gender_table[0]
girl = gender_table[1]

tables = guy.find_all('tbody') # 2 tables of name
#rows = tables[0].find_all('tr')
def get_gender_name(gender):
    """
    provided with gender_table (guy / girl's name), will return / print 
    names in the table
    """
    tables = gender.find_all("tbody")
    get_names(tables[0].find_all('tr'))
    get_names(tables[1].find_all('tr'))

#row = rows[0].find_all('td')