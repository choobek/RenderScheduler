from util.utilities import fileInDirectory

def getFolderPath(lines):
    folderpath = ""
    for line in lines:
        if '&&REM' in line:
            folderpath = line.split("&&REM")[1].strip().split("/")
            folderpath.pop()
            folderpath = '/'.join(folderpath)
    return folderpath

def getFrameRange(lines):
    framerange = ""
    for line in lines:
        if 'hython' in line:
            framerange = line.split("-f")[1].strip().split("-i")[0].strip().split()
            framerange[:] = [s.split('.')[0] for s in framerange]
    return framerange

def getFramePaths(lines, framerange):
    framepaths = []
    temppath = ""
    for line in lines:
        if '&&REM' in line:
            temppath = line.split("&&REM")[1].strip().split('.')
    for frame in range(int(framerange[0]),int(framerange[1])):
        temppath[1] = str(frame).zfill(4)
        framepath = '.'.join(temppath)
        framepaths.append(framepath)
    return framepaths


def parseBatFile(batfile: str):
    file = open(batfile, 'r')
    lines = file.readlines()
    file.close()
    
    #get data
    folderpath = getFolderPath(lines)
    framerange = getFrameRange(lines)
    framepaths = getFramePaths(lines,framerange)

    frames = fileInDirectory(folderpath)
    if len(frames)==0:
        return
    #append folderpath to all items    
    frames[:] = ['/'.join((folderpath,frame)) for frame in frames]
    #set new framerange
    framepaths = set(framepaths).intersection(frames)
    framepaths = sorted(framepaths)
    if len(framepaths)==0:
        return
    framerange[0] = framepaths[-1].split('.')[1].lstrip('0')
    framerange[0] = str(int(framerange[0])+1)
    temppath = ""
    
    if framerange[0] == framerange[1]:
        import os
        os.remove(batfile)
        return

    for line in lines:
        if 'hython' in line:
            temppath = line.split("-f")
            lpath = temppath[0].strip()+" -f "
            temppath = temppath[1].strip().split("-i")
            frame = temppath[0].strip()
            rpath = temppath[1].strip()
            lines[1] = lpath+framerange[0]+' '+framerange[1]+' -i '+rpath+'\n'
    
    file = open(batfile, 'w')
    file.writelines(lines)
    file.close()
    #print(lines)

def parseFolder(watch_dir: str):
    files = fileInDirectory(watch_dir)
    for file in files:
        parseBatFile(watch_dir+'/'+file)
        #print(watch_dir+'/'+file)