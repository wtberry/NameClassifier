"""
This script reads in the list of first names in kanji, and 
look up their phonetic letters in hiragana, as well as sex

- URL: https://b-name.jp/赤ちゃん名前辞典
- when collected, it'll save it in a dictionary with key of the name, and 
value as [] of phonetics.
"""
import os
import csv
import sys
import glob
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

# setup and read in the name list
URL_temp = "https://b-name.jp/赤ちゃん名前辞典/?q={}&mode=2&sex=all"

f = open("first_name_list.csv", "r")
name_list = [line.strip('\n') for line in f]

URL = URL_temp.format("千花")

soup = load_soup(URL)

# tables of 3 in the page, but the first table contains the name and gender
name_table = soup.find_all("table")[0]
rows = name_table.find_all('tr')[1:]

# next iter through the rows for the info, and get the gender from class name