#!/usr/bin/env python

import sys, os, time
from fnmatch import fnmatch
from filecmp import cmp

def localtime(format= "%d%b%H:%M:%S", seconds=None):
    if not seconds:
        seconds = time.time()
    return time.strftime(format, time.localtime(seconds))

def searchAndReplace(toFind, toReplace, fileName):
    filePath = os.path.abspath(fileName)
    print "searchreplace.py running at", localtime()
    print "Replacing '" + toFind + "' with '" + toReplace + "'"
    if os.path.isfile(filePath):
        print "Replacing in", filePath
        newFileName = filePath + ".new"
        newFile = open(newFileName, "w")
        for line in open(filePath):
            newFile.write(line.replace(toFind, toReplace))
        newFile.close()
        if not cmp(filePath, newFileName, 0):
            sys.stdout.flush()
            os.system("diff " + filePath + " " + newFileName)
            print "OK to commit?"
            answer = sys.stdin.readline().strip()
            if answer == "y":
                os.remove(filePath)
                os.rename(newFileName, filePath)
            else:
                os.remove(newFileName)
                print "Not editing the file."
        else:
            os.remove(newFileName) 
    else:
        sys.stdout.write("ERROR: there were no files present matching " + repr(filePath) + "\n")


if len(sys.argv) < 4 or "____" in sys.argv:
    print "Usage : searchreplace.py <toFind> <toReplace> <files>"
else:
    toFind = sys.argv[1]
    toReplace = sys.argv[2].replace("\\n", "\n")
    pattern = sys.argv[3]
    searchAndReplace(toFind, toReplace, pattern)

