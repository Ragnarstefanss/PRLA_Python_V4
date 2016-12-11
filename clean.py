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
                tvList.append(name)
                newPath = processTvShowName(name)
                newName = " ".join(newPath.split())
                print (newName[:30])
                #if not os.path.exists(downloads + "/../sorted/TV_shows/"+newPath):
                    #shutil.move(os.path.join(subdir, file), downloads + "/../sorted/TV_shows/"+newPath)
            #Setja inn ombd dótið til að filtera út kvikmyndir og setja þær í sér möppu
            else:
                shutil.move(os.path.join(subdir, file), downloads + "/../sorted/unrecognized/"+file.title())
        
def processTvShowName(name):
    
    #TODO: implementlll
    #Endurformatta nafn þáttar til að losna við punkta og strik og slíkt úr nafni, nafn = allt á undan S01E01 etc.
    #Skila nafni skráar, nafni þáttar og seríunúmeri
    #Helst formatta skilagildi sem enda áframhald á pathi frá TV_shows
    #return name
    take_out = [".Avi", "Zernicus", "S1", "S2", "S3" , "S4", "S5", "S6", "S7", "S8", "S9", "{ www.Torrentday.com ]", "Ws", "Pdtv", "[Skid]", "Tvrip",
                "720P", "Aac2", "X264","Nfrip", "Hdtv", "Lol", "Asa", ".Hdtv", "Special", "W4F", "Fever",
                "Tla", "Afg", ".[Vtv]", "Dimension", "Crimson", "Orenji", "  W4", "Aaf", ".Sample", ".Mp4", ".Reenc Max.", "-", ".", "Sample", "Ftp", "Reenc",
                "Max", "Mkv", "Ange", "angelic", "Xvid", 'Uncut', "2Hd", "Fqm", "C4T", "Tvchaos", "Benidor", "2H", "M4V", "Fqm", "Slowap", "Evolve",
                "_", "Fov", "Immerse", "Cbm", "Srt", "Killers", "Fum"]
    
    for value in take_out:
        name = name.replace(value," ")
    for i in range(1950, 2050):
        if str(i) in name:
            name = name.replace(str(i)," ")


    #name=name.lstrip()
    #name=name.rstrip()

    return name

