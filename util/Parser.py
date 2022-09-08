class Parser:
    def __init__(self, watchdir, processname, separator):
        self.watchdir = watchdir        
        self.processname = processname
        self.separator = separator
        
    def get_folder_path(self, textlines):
        folderpath = ""
        for textline in textlines:
            if self.separator in textline:
                folderpath = textline.split(self.separator)[1].strip().split("/")
                folderpath.pop()
                folderpath = '/'.join(folderpath)
        return folderpath

    def get_frame_range(self, textlines):
        framerange = ""
        for textline in textlines:
            if self.processname in textline:
                framerange = textline.split("-f")[1].strip().split("-i")[0].strip().split()
                framerange[:] = [s.split('.')[0] for s in framerange]
        return framerange
    
    def get_frame_paths(self, textlines, framerange):
        framepaths = []
        temppath = ""
        for textline in textlines:
            if self.separator in textline:
                temppath = textline.split(self.separator)[1].strip().split('.')
        for frame in range(int(framerange[0]),int(framerange[1])):
            temppath[1] = str(frame).zfill(4)
            framepath = '.'.join(temppath)
            framepaths.append(framepath)
        return framepaths
    
    def rewrite_frame_range(self, filepath):
        print('Checking if ' + filepath + ' needs a frame range rewrite...')
        # REWRITE FRAME RANGE IN BAT FILE
        # parse data to variables
        file = open(filepath,'r')
        textlines = file.readlines()
        file.close()
        folderpath = self.get_folder_path(textlines)
        framerange = self.get_frame_range(textlines)
        framepaths = self.get_frame_paths(textlines, framerange)
        # check if there are some already rendered frames
        from util.utilities import file_in_directory
        frames = file_in_directory(folderpath)
        if len(frames) == 0:
            return
        # append folderpath to all items
        frames[:] = ['/'.join((folderpath,frame)) for frame in frames]
        # set new framerange
        framepaths = set(framepaths).intersection(frames)
        framepaths = sorted(framepaths)
        if len(framepaths)==0:
            return
        framerange[0] = framepaths[-1].split('.')[1].lstrip('0')
        framerange[0] = str(int(framerange[0])+1)
        temppath = ""
        # remove file if actual frame is the last frame
        if framerange[0] == framerange[1]:
            import os
            os.remove(filepath)
            return
        # prepare the content of new bat file
        for textline in textlines:
            if self.processname in textline:
                temppath = textline.split("-f")
                lpath = temppath[0].strip()+" -f "
                temppath = temppath[1].strip().split("-i")
                #frame = temppath[0].strip()
                rpath = temppath[1].strip()
                textlines[1] = lpath+framerange[0]+' '+framerange[1]+' -i '+rpath+'\n'
        # rewrite the file
        file = open(filepath, 'w')
        file.writelines(textlines)
        file.close()
        print('New frame range: [' + framerange[0] + ' - ' + framerange[1] + '] on file ' + filepath)

