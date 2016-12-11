import os
import re
#import string
import json
import urllib.request
import shutil



def clean(downloads, sorted):
    tvList = []
    for subdir, dirs, files in os.walk(downloads):
        for file in files:
            name = file.title()
            #wow, so read. very understand
            #Regular expressions, in order of execution, for: files with extensions that are to be deleted,
            #.Part files, which are partial downloads and are therefore to be left alone
            #Files in audio formats, to be moved to sorted/audio
            #Files containing S01E01 or similar episodic syntax denoting that it is part of a series, to be put into sorted/TV_shows
            #Files not matching any of these will be put into sorted/unrecognized
            match = re.compile("(?!.*(\.[Jj]pg$|\.[Rr]ar$|\.[Zz]ip$|\.[Mm]p3$|\.[Ii]gnore$|\.[Nn]fo$|.[R]\d{1,3}$|\.[Dd]at$|"
                               "\.[Pp]ng$|\.[Ll]nk$|\.[Pp]ar[t\d*]$|\.[Ss]vf$|\.[Ss]fv$|\.[Mm]ta$|\.[Tt]xt$|"
                               "\.[Ww]av$))(\d{1,2}[Xx]\d{1,2}|\[\d{1,3}\.\d{1,3}\]|[Ee][Pp]\d{1,3}|- \d{2} -|- \d{2,3}|"
                               "\.\d{3}\.|[Ss]\d{1,3} [Ee] {0,1}\d{1,3}|[\. ]{0,1}[Pp]ilot[\. ]{0,1}]|"
                               "[Ss]eason {0,1}\d{1,2}[ -]{1,3}[Ee]pisode {0,1}\d{1,2}|#\d{1,3}|[Ss]\d{1,2}.([Ee]xtra)?([Ss]pecial)?)")
            match1 = re.compile("\.Part$")
            match2 = re.compile("\.[Jj]pg|\.[Rr]ar|\.[Zz]ip|\.[Ii]gnore|\.[Nn]fo|.[R]\d{1,3}|\.[Dd]at|\.[Pp]ng|\.[Ll]nk|\.[Ss]vf|\.[Ss]fv|\.[Mm]ta|"
                                "\.[Tt]xt|\.[Ss]tyle|\.[Tt]orrent")
            match3 = re.compile("\.[Mm]p3$|\.[Ww]av$")

            if match2.search(name):
                os.remove(os.path.join(subdir, file))
            elif match1.search(name):
                continue
            elif match3.search(name):
                shutil.move(os.path.join(subdir, file), downloads + "/../sorted/audio/"+file.title())
            elif match.search(name):
                index = match.search(name).start()
                endindex = match.search(name).end()
                print(name)
                print(index)
                tvList.append(name)
                newPath = processTvShowName(name[:index], name[index:endindex])
                newName = name
                #print (newName[:30])
                if not os.path.exists(downloads + "/../sorted/TV_shows/" + newPath):
                    os.mkdir(downloads + "/../sorted/TV_shows/" + newPath)
                if not os.path.exists(downloads + "/../sorted/TV_shows/"+newPath+"/"+ newName):
                    shutil.move(os.path.join(subdir, file), downloads + "/../sorted/TV_shows/"+newPath+"/"+newName)
            #Setja inn ombd dótið til að filtera út kvikmyndir og setja þær í sér möppu
            else:
                shutil.move(os.path.join(subdir, file), downloads + "/../sorted/unrecognized/"+file.title())
    for show in tvList:
        print(show)
        
def processTvShowName(name, seasons):
    
    #TODO: implementlll
    #Endurformatta nafn þáttar til að losna við punkta og strik og slíkt úr nafni, nafn = allt á undan S01E01 etc.
    #Skila nafni skráar, nafni þáttar og seríunúmeri
    #Helst formatta skilagildi sem enda áframhald á pathi frá TV_shows
    
    take_out = ["_", "[", "]", ".", " -"]
    arr = []
    for value in take_out:
        name = name.replace(value," ")
        arr.append(name)
    for i in range(1920, 2050):
        if str(i) in name:
            name = name.replace(str(i)," ")
            arr.append(name)
    
    #shows = re.findall(r"""(.*)[ .]S(\d{1,2})E(\d{1,2})""", name, re.VERBOSE)
        
    return name.rstrip()

