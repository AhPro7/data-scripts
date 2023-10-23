# this file will copy files from csv to a new folder
# the csv file should have the following format: video_id ==> name without extension e.g. 87dF ==> 87dF.wav

import os
import shutil
import pandas as pd

# read csv file
csv = input("Enter csv file path from home: ")
data = pd.read_csv(csv)

persntage = input("Enter percentage of data to copy: ")
# get the number of rows
rows = data.shape[0]
# get the number of rows to copy
rows_to_copy = int((int(persntage)/100)*rows)

# randomlly select rows to copy
rows_to_copy = data.sample(rows_to_copy)

# get the path of the folder to copy from
path = input("Enter path of the folder to copy from: ")
# get the path of the folder to copy to
path_to = input("Enter path of the folder to copy to: ")

# loop through the rows and copy the files
from tqdm import tqdm

for index, row in tqdm(rows_to_copy.iterrows()):
    # get the name of the file
    name = row['video_id']
    # get the path of the file
    file_path = os.path.join(path, name+'.wav')
    # get the path of the file to copy to
    file_path_to = os.path.join(path_to, name+'.wav')
    # copy the file
    shutil.copyfile(file_path, file_path_to)

# to make reqeriments.txt file run the following command
# pip freeze > requirements.txt 
# to install the reqeriments.txt file run the following command


