import os
import zipfile
import shutil
shutil.rmtree("downloads")
shutil.rmtree("sorted")
os.makedirs("sorted")
os.makedirs("sorted/TV_shows")
os.makedirs("sorted/unrecognized")
os.makedirs("sorted/audio")
zip = zipfile.ZipFile("downloads.zip")
zip.extractall()
zip.close()