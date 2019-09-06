import pandas as pd
import os
import glob
import csv

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
#print(file_list)

# read in each csv, and add the last name column
def get_df(f):
    """given path to the file, return dataframe with last name
    """
    df = pd.read_csv(f)
    last = df.columns[0]
    df.columns = ['name']
    df['last'] = last
    return df

# make it into generator 
df_generator = (get_df(f) for f in file_list)


# concat to one big dataframe
df = pd.concat(df_generator, axis=0, ignore_index=True)
print("Original dataset size before processing: ", df.shape)

# filter out the names that contains last name
def is_last_in_name(row):
    return 1 if row['last'] in row['name'] else 0

# adding a column that is 1 when last name is present in the name, 0 otherwise
df["name_contains_last"] = df.apply(is_last_in_name, axis=1) 
df = df[df['name_contains_last'] == 1]

# removing the ()s entry in the name, and leaving the rest
df['name'] = df['name'].str.replace(r"\(.*\)", "")


# separating first and last name
def separate(row):
    """Separate first and last names, and return first name"""
    return row['name'].split(row['last'])[-1]

df['first'] = df.apply(separate, axis=1)


# examine what kind of character the first name contains, and put info in a column
hiragana = "[\u3040-\u309F]"
katakana = "[\u30A0-\u30FF]"

df['first_char'] = 'kanji'

df.loc[df['first'].str.contains(hiragana), 'first_char'] = 'hira'
df.loc[df['first'].str.contains(katakana), 'first_char'] = 'kata'

# clean up the white space
df['name'] = df['name'].str.strip()
df['last'] = df['last'].str.strip()
df['first'] = df['first'].str.strip()

## now extract the unique first name list with kanji
first_name_list = list(df[df['first_char'] == 'kanji']['first'].unique())

# write on csv
f = open("first_name_list.csv", "w")
writer = csv.writer(f)
for name in first_name_list:
    writer.writerow([name])

df.to_csv("all_names.csv", index=False)

print("Done, first name writtene to {}".format("first_name_list.csv"))


## Now using the website, get the furigana