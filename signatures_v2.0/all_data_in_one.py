import shutil
import os

path2 = "C:/Users/User/Desktop/Desktop/SIGNATURE_v2.0/data/train"
path = "C:/Users/User/Desktop/Desktop/SIGNATURE_v2.0/prepare_data/signatures"

for foldername in os.listdir(path):
        i = 0
        for filename in os.listdir(path + '/' + foldername):
            shutil.copy2((path + '/' + foldername + '/' + filename), path2) 