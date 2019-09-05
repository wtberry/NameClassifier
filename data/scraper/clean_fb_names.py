import pandas as pd
import os
import glob

"""
Script to clean up the fb collected names, and return list of unique Japanese first names.

Concretely, this script:

    - load the data into Pandas dataframe
    - set the last name as row index
    - clean methods() in which
        - filter out the records that contains last name string in the entry
        - check the position of the last name string
        - check for white space between the last and first name
        - split the entry into last, and first name
        - extract unique first name only
        - with the 人名辞典, get the phenotic letters for each first name (Kanji ones) and organize it into dictionary
"""

# create path and list of files to load
path = os.getcwd()
ext = "fb_names/*_names.txt"
print(os.path.join(path, ext))

file_list = glob.glob(os.path.join(path, ext))
print(file_list)

# create a generator for reading in the files, skip the first row and put 'name' as col name
df_generator = (pd.read_csv(f, header=0, names=['name']) for f in file_list)

# concat to one big dataframe
df = pd.concat(df_generator, axis=0, ignore_index=True)

## or crate a table with last name as index and name as column

