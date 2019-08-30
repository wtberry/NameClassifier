import pandas as pd
import os
import glob

"""
Just a script to load all the name files in fb_names/ dir as one big dataframe
"""

# create path and list of files to load
path = os.getcwd()
ext = "*_names.txt"

file_list = glob.glob(os.path.join(path, ext))

# create a generator for reading in the files, skip the first row and put 'name' as col name
df_generator = (pd.read_csv(f, header=0, names=['name']))

# concat to one big dataframe
df = pd.concat(df_generator, axis=0, ignore_index=True)

## or crate a table with last name as index and name as column

