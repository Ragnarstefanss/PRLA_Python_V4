import os
import re
#import string
import json
import urllib.request
import shutil



def clean(downloads, sorted):
    tvList = []
    # wow, so read. very understand
    # Regular expressions, in order of execution, for: files with extensions that are to be deleted,
    # .Part files, which are partial downloads and are therefore to be left alone
    # Files in audio formats, to be moved to sorted/audio
    # Files containing S01E01 or similar episodic syntax denoting that it is part of a series, to be put into sorted/TV_shows
    # Files not matching any of these will be put into sorted/unrecognized
    episodesyntax = re.compile("(?!.*(\.[Jj]pg$|\.[Rr]ar$|\.[Zz]ip$|\.[Mm]p3$|\.[Ii]gnore$|\.[Nn]fo$|.[R]\d{1,3}$|\.[Dd]at$|"
                       "\.[Pp]ng$|\.[Ll]nk$|\.[Pp]ar[t\d*]$|\.[Ss]vf$|\.[Ss]fv$|\.[Mm]ta$|\.[Tt]xt$|"
                       "\.[Ww]av$))(\d{1,2}[Xx]\d{1,2}|\[\d{1,3}\.\d{1,3}\]|[Ee][Pp]\d{1,3}|- \d{2} -|- \d{2,3}|"
                       "\.\d{3}\.|[Ss]\d{1,3} [Ee] {0,1}\d{1,3}|[\. ]{0,1}[Pp]ilot[\. ]{0,1}]|"
                       "[Ss]eason {0,1}\d{1,2}[ -]{1,3}[Ee]pisode {0,1}\d{1,2}|#\d{1,3}|[Ss]\d{1,2}.([Ee]xtra)?([Ss]pecial)?)")
    partialdownloads = re.compile("\.Part$")
    tobedeleted = re.compile("\.[Jj]pg|\.[Rr]ar|\.[Zz]ip|\.[Ii]gnore|\.[Nn]fo|.[R]\d{1,3}|\.[Dd]at|\.[Pp]ng|\.[Ll]nk|\.[Ss]vf|\.[Ss]fv|\.[Mm]ta|"
        "\.[Tt]xt|\.[Ss]tyle|\.[Tt]orrent")
    audio = re.compile("\.[Mm]p3$|\.[Ww]av$")

    foldersyntax = re.compile("[Ss]eason[\. -]{0,1}\d{1,2}")

    for subdir, dirs, files in os.walk(downloads):
        for dir in dirs:
            folder = dir.title()
            if foldersyntax.search(folder):
                index = foldersyntax.search(folder).start()
                name = folder[:index - 1]
                new_name = name.rstrip()
                if not os.path.exists(sorted + "/TV_shows/" + new_name):
                    os.mkdir(sorted + "/TV_shows/" + new_name)
                if not os.path.exists(sorted + "/TV_shows/" + new_name + "/" + folder[index:]):
                    shutil.move(os.path.join(subdir, dir), sorted + "/TV_shows/" + new_name + "/" + folder[index:])
                    
    for subdir, dirs, files in os.walk(downloads):
        for file in files:
            name = file.title()
            if tobedeleted.search(name):
                os.remove(os.path.join(subdir, file))
            elif partialdownloads.search(name):
                continue
            elif audio.search(name):
                shutil.move(os.path.join(subdir, file), sorted + "/audio/"+file.title())
            elif episodesyntax.search(name):
                index = episodesyntax.search(name).start()
                endindex = episodesyntax.search(name).end()
                print(name)
                print(index)
                tvList.append(name)
                newPath = processTvShowName(name[:index], name[index:endindex])
                newName = name
                #print (newName[:30])
                if not os.path.exists(sorted + "/TV_shows/" + newPath):
                    os.mkdir(sorted + "/TV_shows/" + newPath)
                if not os.path.exists(sorted + "/TV_shows/"+newPath+"/"+ newName):
                    shutil.move(os.path.join(subdir, file), sorted + "/TV_shows/"+newPath+"/"+newName)
            #Setja inn ombd dótið til að filtera út kvikmyndir og setja þær í sér möppu
            else:
                shutil.move(os.path.join(subdir, file), sorted + "/unrecognized/"+file.title())
    #for subdir, dirs, files in os.walk(sorted + "/unrecognized/"):
     #   for file in files:

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


def api(name):
    url = str("http://www.omdbapi.com/?t=" + name)

    read_data = urllib.request.urlopen(url)
    load = json.loads(read_data.read().decode(read_data.info().get_param('charset') or 'utf-8'))

    api_title = "None"
    api_type = "None"
    if load["Response"] == "True":
        api_title = load["Title"]
        api_type = load['Type']

    else:
        print('could not find tv series / movie %s' % name)
    return (api_title, api_type)