import os
import re
#import string
#import json
#import urllib
import shutil
def clean(downloads, sorted):
    tvList = []
    for subdir, dirs, files in os.walk(downloads):
        for file in files:
            name = file.title()
            match = re.compile("(?!.*(\.[Jj]pg|\.[Rr]ar|\.[Zz]ip|\.[Mm]p3|\.[Ii]gnore|\.[Nn]fo|.[R]\d{1,3}|\.[Dd]at|\.[Pp]ng|\.[Ll]nk|"
                               "\.[Pp]ar[t\d*]|\.[Ss]vf|\.[Ss]fv|\.[Mm]ta|\.[Tt]xt|\.[Ww]av))[Ss]?\d{1,2}x?[Ee]?[^\d\._ -]\d{1,3}")
            if match.search(name):
                tvList.append(name)
                newPath = processTvShowName(name)
                if not os.path.exists("/Users/kristinn/PycharmProjects/PRLA/PRLA_Python_V4/sorted/TV_shows/"+newPath):
                    shutil.move(os.path.join(subdir, file), "/Users/kristinn/PycharmProjects/PRLA/PRLA_Python_V4/sorted/TV_shows/"+newPath)
    for show in tvList:
        print(show)
    return

def processTvShowName(name):
    #TODO: implement
    #Endurformatta nafn þáttar til að losna við punkta og strik og slíkt úr nafni, nafn = allt á undan S01E01 etc.
    #Skila nafni skráar fegruðu, nafni þáttar og seríunúmeri
    #Helst formatta skilagildi sem enda áframhald á pathi frá TV_shows
    return name
    


#
    # def main(mypath, destination):
    # myndir = []
    # listi = []
    # strengur = ''

    # for (dirpath, dirnames, filenames) in os.walk(mypath):
    #     myndir.extend(filenames)
    #     break

    ##    for l in myndir:
    ##        print (l)
    ##
    # print(myndir)

    # name = "12 Years a Slave"
    # year = 0
    # if year != 0:
     #    url = "http://www.omdbapi.com/?t=" + name + "&y=" + str(year)
    # else:
     #    url = "http://www.omdbapi.com/?t=" + name

    # url_values = json.loads(urllib.urlopen(url).read())



# Fá nafn á mynd/þætti
# fara í gegnum allar undir möppur
# Leita í omdbapi að nafninu með search string
# skoða "Type": "series" / "Type": "movies"
# ef bíó mynd setja skránna inn í ../temp/movies
# ef sjónvarpsþáttur setja skránna inn í ( ../temp/series/[SHOW_NAME]/[SEASON_NUMBER]/[episode] )


# ef skrá ekki lesanleg þá má eyða henni (aka .jpg , .rar, .zip)