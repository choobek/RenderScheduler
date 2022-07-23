from os import listdir
from os.path import isfile, join

#function to return files in a directory
def fileInDirectory(watchDirectory: str):
    onlyfiles = [f for f in listdir(watchDirectory) if isfile(join(watchDirectory, f))]
    return(onlyfiles)

#function comparing two lists

def listComparison(OriginalList: list, NewList: list):
    differencesList = [x for x in NewList if x not in OriginalList] #Note if files get deleted, this will not highlight them
    return(differencesList)

def doThingsWithNewFiles(newFiles: list):
    for newFile in newFiles:
        parseBatFile(newFile)
    print(f'I would do things with file(s) {newFiles}')

import time

def fileWatcher(watchDirectory: str, pollTime: int):
    while True:
        if 'watching' not in locals(): #Check if this is the first time the function has run
            previousFileList = fileInDirectory(watchDirectory)
            watching = 1
        
        time.sleep(pollTime)
        
        newFileList = fileInDirectory(watchDirectory)
        
        fileDiff = listComparison(previousFileList, newFileList)
        
        previousFileList = newFileList
        if len(fileDiff) == 0: continue
        doThingsWithNewFiles(fileDiff)