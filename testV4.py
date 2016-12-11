import shutil
import os
import zipfile
import clean
shutil.rmtree("downloads")
shutil.rmtree("sorted")
os.makedirs("sorted")
os.makedirs("sorted/TV_shows")
os.makedirs("sorted/unrecognized")
zip = zipfile.ZipFile("downloads.zip")
zip.extractall()
zip.close()
clean.clean("downloads", "sorted")