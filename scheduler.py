# Initial Parameters
WATCH_DIR = r'C:/Users/choob/Desktop/batch'
PROCESS_NAME = 'hython'
# GPU CHECK LISTING TIME (in seconds) = review_time * queue_iter
REVIEW_TIME = 6
QUEUE_ITER = 100
#
GPU_IDLE_LIMIT = 0.4
GPU_INIT_LIST = 1
GPU_TO_MONITOR = 0

from util.parsing import parseFolder
from util import utilities
import subprocess
import time
import GPUtil
import math

def checkFileCount():
    # Close if there are no files to render
    files = utilities.fileInDirectory(WATCH_DIR)
    return len(files)

def setupRendering():
    if checkFileCount()>0:
        if utilities.checkIfProcessRunning(PROCESS_NAME)==False:
            '''Setup whole rendering'''
            print('Setup rendering...')
            
            parseFolder(WATCH_DIR)

            files = utilities.fileInDirectory(WATCH_DIR)
            if files:
                p = subprocess.run(WATCH_DIR+'/'+files[0], shell=True)
        else:
            utilities.cleanTheProcesses(PROCESS_NAME)

def monitorProcess():
    running = True
    
    loadlist = []
    utilities.fillList(loadlist,QUEUE_ITER,GPU_INIT_LIST)

    while utilities.checkIfProcessRunning(PROCESS_NAME):
        gpus = GPUtil.getGPUs()
        if (len(loadlist)<QUEUE_ITER):
            loadlist.append(gpus[GPU_TO_MONITOR].load)
        else:
            loadlist.pop(0)
        average_load = utilities.average(loadlist)
        print(loadlist)
        print(average_load)
        if (average_load<GPU_IDLE_LIMIT):
            print('GPU_IDLE_LIMIT has been exceeded')
            break

        print('Rendering is Running...waiting.')
        time.sleep(REVIEW_TIME) # Wait and try again
        print('Checking again...')
    
    print('Rendering is not running, good to go.')


while(True):


    # Setup first instance
    setupRendering()

    # Check if there are files to schedule and break if not
    if checkFileCount()==0: break

    # Monitor the rendering
    monitorProcess()





