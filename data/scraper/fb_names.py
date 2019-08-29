import csv
import time
import pandas as pd
import selenium
from selenium import webdriver
import ray

"""Using selenium web browser driver, 
This script will search for the facebook profiles from last name list on the 
last_names.csv, and extract full names, clean up and store it as csv.

Search will be on the search page, and will scroll the page infinetely until 
the given numbers of data are collected

Param:
    Last name: string of last name to search
    num: numbers of names to store per given last name. (Non unique)


Look up the populations of FB users in Japan, and 
see how many profiles I need to sample, in order to get statistically correct sample.

And combine it with the data of ratio of last names to determine how many results are needed
for each given last names. 

last_name_sample_size = Total_fb_usr * sample_rate * last_name_ratio

## Better to scroll all the way down first 
then find_elements()


## Credit for infinite scrolling 
https://gist.github.com/artjomb/07209e859f9bf0206f76
"""

return_height = "return document.body.scrollHeight"
scroll = "window.scrollTo(0, document.body.scrollHeight);"
# numbers of names included in a page after # of scroll
# scroll numbre is the index of the list

# start the multiprocessing lib ray
ray.shutdown()
ray.init()

@ray.remote(num_cpus=4)
def scrape_write(last, pause=1, NUM=100):
    """
    Access facebook through selenium wtih given URL  and search for profiles of given last name, and write the list of names on the txt file, under
    fb_names/*txt
    Param:
        NOT PASSING THIS anymore,browser: selenium chrome webdriver, browser to access the fb
        last: last name string to look up
        pause: pause time (float/int) between scrolling further for more result on search page
        NUM: int, how many times to scroll the search page
    """

    browser = webdriver.Chrome()
    URL_temp = "https://ja-jp.facebook.com/public/"
    URL = URL_temp+last    

    print("#### {} ####".format(last))
    # start browser
    #browser = webdriver.Chrome()
    # refresh page
    browser.get(URL)
    print(browser.title)

    lastHeight = browser.execute_script(return_height)
    print("last height: ", lastHeight)
    num_names_per_scroll = [] 
    for i in range(NUM):
        # scroll page
        browser.execute_script(scroll)
        time.sleep(pause)
        newHeight = browser.execute_script(return_height)
        # check if it's the bottom of the page
        """
        if newHeight == lastHeight:
            break
        """
        lastHeight = newHeight
        print(i)
    # get the names from the entire scrolled page
    tags = browser.find_elements_by_tag_name("span")
    
    fileName = "fb_names/{}_names.txt".format(last)
    # now open and write on file
    f = open(fileName, 'a')
    writer = csv.writer(f)

    # write the header
    writer.writerow([last])
    # skip the first element, which is a Matawa
    for tag in tags:
        name = tag.text
        if len(name) < 3  or name == "または":
            # do nothing
            pass
        else:
            print("saving: ", name)
            writer.writerow([name])
    f.close()
    browser.close()



## Read in the last name data
last = pd.read_csv('../last_names.csv')
lasts = list(last['last_name'])

NUM = 500
# go through a list of last names and collect full names
num_lasts = int(len(lasts)/2) # go through half of the last name, which covers the 90% and more of the population
print("starting stopwatch")
start = time.time()

## Open browser and start scraping
for last in lasts:
    tags = scrape_write.remote(last, pause=1, NUM=NUM)
    #tags = scrape_write(last, pause=1, NUM=5)

# done scraping, display the time spent

print("stoping the stopwatch")
finish = time.time()
spent = finish - start
print(spent, "seconds")