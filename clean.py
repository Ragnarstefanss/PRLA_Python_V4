import os
def clean(downloads, sorted):
    for subdir, dirs, files in os.walk(downloads):
        