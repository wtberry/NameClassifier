import requests
from bs4 import BeautifulSoup as bs
import csv
import re
import sys

"""
This script scrape list of last names from most popular to least, as a ranking and distribution data.

Each page includes 500 names, and there are 80 pages. 
URL is structured so that https://myoji ....... page=NUMBER where NUMBER is from 0~79
"""

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


def scrape(URL):
    """
    scrape from the website, get the soup, and
    return lists of string of name, it's popularity and population with \n characters
    """

    # setting up variables
    #URL = "https://myoji-yurai.net/prefectureRanking.htm;jsessionid=C13440C475D5A9E10ACD0C8C63AF6E6C.jvm1"
    # get the response from url
    
    # get soup
    soup = load_soup(URL)
    
    # get tbody tags
    tbodies = soup.find_all('tbody')
    
    # pythonic 9, and 10th tag contains the name list
    twenty, five = tbodies[9].text.split('\n\n\n'), tbodies[10].text.split('\n\n\n')
    twenty[0] = twenty[0].strip('\n\n')
    twenty[-1] = twenty[-1].strip('\n\n')
    five[0] = five[0].strip('\n\n')
    five[-1] = five[-1].strip('\n\n')
    return twenty, five

# clean up the list of names and its associated data
def clean(names):
    """remove unnecesary letters, encapsulate each record in a list within a list, returns 2D list"""
    return [i.replace('位', '').replace('およそ', '').replace('人','').replace(',','').split('\n') for i in names]


def write_csv(names, fname, append=True):
    """write to csv file"""
    app = 'a' if append==True else 'w'
    with open(fname, app) as writeFile:
        writer = csv.writer(writeFile)
        for line in names:
            writer.writerow(line)
    writeFile.close()


if __name__ == "__main__":
    TOTAL_PAGE = 80
    for i in range(TOTAL_PAGE):
        if i%10 == 0:
            print("loading {}th page".format(i))
        # make URL
        URL = "https://myoji-yurai.net/prefectureRanking.htm?prefecture=%E5%85%A8%E5%9B%BD&page=" + str(i)
        twenty, five = scrape(URL)
        twenty = clean(twenty)
        five = clean(five)
    
        write_csv(twenty, 'last_names.csv', append=True)
        write_csv(five, 'last_names.csv', append=True)

