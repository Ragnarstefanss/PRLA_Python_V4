import shutil
import os
import zipfile
#import clean
shutil.rmtree("downloads")
shutil.rmtree("sorted")
os.makedirs("sorted")
zip = zipfile.ZipFile("downloads.zip")
zip.extractall()
zip.close()
#clean.clean("/Users/kristinn/PycharmProjects/PRLA/PRLA_Python_V4/downloads", "/Users/kristinn/PycharmProjects/PRLA/PRLA_Python_V4/sorted")