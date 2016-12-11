import os
import re
import json
import urllib.request
import shutil



def clean(downloads, sorted):
    tvList = []
    # wow, so read. very understand
    # These are regular expressions, in order of execution, for: files with extensions that are to be deleted,
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
        "\.[Tt]xt|\.[Ss]tyle|\.[Tt]orrent|\.[Ss]mi$|\.[Pp]art?\d{1,2}$")
    audio = re.compile("\.[Mm]p3$|\.[Ww]av$")

    foldersyntax = re.compile("[Ss]eason[\. -]{0,1}\d{1,2}")

    yearsyntax = re.compile("[\[\.( -]{0,2}\d{4}")

    tvfolder = "/TV_shows/"
    audiofolder = "/Audio/"
    unsortedfolder = "/Unrecognized/"
    moviefolder = "/Movies/"

    #loop through the folders, if any look like they contain whole seasons, move them, as they are, accordingly
    for subdir, dirs, files in os.walk(downloads):
        for dir in dirs:
            folder = dir.title()
            if foldersyntax.search(folder):
                index = foldersyntax.search(folder).start()
                name = folder[:index - 1]
                new_name = name.rstrip()

                if not os.path.exists(sorted + tvfolder + new_name):
                    os.mkdir(sorted + tvfolder + new_name)
                if not os.path.exists(sorted + tvfolder + new_name + "/" + folder[index:]):
                    shutil.move(os.path.join(subdir, dir), sorted + tvfolder + new_name + "/" + folder[index:])

    #loop through the files, if it looks like a tv show, move it accordingly etc.
    for subdir, dirs, files in os.walk(downloads):
        for file in files:
            name = file.title()

            if tobedeleted.search(name):
                os.remove(os.path.join(subdir, file))

            elif partialdownloads.search(name):
                continue

            elif audio.search(name):
                shutil.move(os.path.join(subdir, file), sorted + audiofolder +file.title())

            elif episodesyntax.search(name):
                index = episodesyntax.search(name).start()
                tvList.append(name)
                newPath = processTvShowName(name[:index])
                newName = name

                if not os.path.exists(sorted + tvfolder + newPath):
                    os.mkdir(sorted + tvfolder + newPath)
                if not os.path.exists(sorted + tvfolder + newPath + "/"+ newName):
                    shutil.move(os.path.join(subdir, file), sorted + tvfolder +newPath+"/"+newName)
            else:
                shutil.move(os.path.join(subdir, file), sorted + unsortedfolder +file.title())

    #loop through the things that could not be sorted. Try to get titles preceding years and send those as
    #requests to omdbapi.com to see if they recognize any movie or tv show titles. If so, move accordingly
    for subdir, dirs, files in os.walk(sorted + unsortedfolder):
        for file in files:
            name = file.title()
            
            if yearsyntax.search(name):
                index = yearsyntax.search(name).start()
                name = name[:index]
                take_out = ["_", "[", "]", ".", " -", " "]
                for ch in take_out:
                    name = name.replace(ch, "+")
                if len(name) == len(name.encode()):
                    titletype = api(name)
                    if titletype[0] != "None":
                        if titletype[1] == "movie":
                            if not os.path.exists(sorted + moviefolder + titletype[0]):
                                shutil.move(os.path.join(subdir, file), sorted + moviefolder + file.title())

                        if titletype[1] == "series":
                            if not os.path.exists(sorted + tvfolder + titletype[0]):
                                shutil.move(os.path.join(subdir, file), sorted + tvfolder + file.title())


def processTvShowName(name):
    # Array of items that are typically found in file names
    take_out = ["_", "[", "]", ".", " -"]

    # if there exists an item in name that should not be there then we have to replace it with whitespace
    for value in take_out:
        name = name.replace(value," ")
    # if a file contains a year in it, like if the file is a movie
    # then we have to remove it, so we can use the name as a parameter when using a api to imdb
    for i in range(1920, 2050):
        if str(i) in name:
            name = name.replace(str(i)," ")
    # We return the title of a movie/tv show and watch out that there is no space at the end of the name
    return name.rstrip()


def api(name):
    #Asks omdbapi if name is the title of some known movie or tv show
    #if so, return the title and type (movie, series...)
    url = str("http://www.omdbapi.com/?t=" + name)

    read_data = urllib.request.urlopen(url)
    load = json.loads(read_data.read().decode(read_data.info().get_param('charset') or 'utf-8'))

    api_title = "None"
    api_type = "None"
    if load["Response"] == "True":
        api_title = load["Title"]
        api_type = load['Type']

    return (api_title, api_type)
