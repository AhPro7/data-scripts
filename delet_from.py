# delet persntage of files in a directory

import os
import shutil
import random
per = input("Enter percentage of files to delete: ")
# get the path of the folder to copy from
path = input("Enter path of the folder to delete from: ")

# get the number of files in the folder
files = os.listdir(path)
# get the number of files to copy
files_to_delete = int((int(per)/100)*len(files))

# randomlly select files to copy
files_to_delete = random.sample(files, files_to_delete)

# loop through the files and copy the files
from tqdm import tqdm

for file in tqdm(files_to_delete):
    # get the path of the file
    file_path = os.path.join(path, file)
    # delete the file
    os.remove(file_path)

# to update and download the new file from github run the following command

ubuntu@ip-172-31-26-248:~/Desktop$ git add .
UnboundLocalError
orgin
origin