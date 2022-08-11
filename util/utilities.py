def average(lst):
    return sum(lst) / len(lst)

def fillList(lst, list_length, init_val):
    for i in range(1, list_length+1):
        lst.append(init_val)
    return lst

def fileInDirectory(watchDirectory: str):
    from os import listdir, mkdir
    from os.path import isfile, join, isdir
    if isdir(watchDirectory)==False:
        mkdir(watchDirectory)
    onlyfiles = [f for f in listdir(watchDirectory) if isfile(join(watchDirectory, f))]
    return(onlyfiles)


def checkIfProcessRunning(processName):
        '''Check if there are any running process that contains the given name processName.
        Iterate over the all the running process'''
        print('Checking if rendering is running...')
        import psutil
        for proc in psutil.process_iter():
                try:
                        #print(proc.name().lower())
                        # Check if process name contains the given name string.
                        if processName.lower() in proc.name().lower():
                                return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
        return False

def cleanTheProcesses(processName):
        '''Iterate over all processes and kill every instance which name contains PROCESSNAME'''
        print('Cleaning the processes...')
        import psutil
        for proc in psutil.process_iter():
                try:
                        #print(proc.name().lower())
                        # Check if process name contains the given name string.
                        if processName.lower() in proc.name().lower():
                                proc.kill()
                                return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
        return False

def monitorProcess(processName,gpu_check_freq,gpu_review_time):
        '''Check if there are any running process that contains the given name processName.
        Iterate over the all the running process'''
        print('Monitor process...')
        import psutil
        import GPUtil
        import time
        for proc in psutil.process_iter():
                try:
                        # Check if process name contains the given name string.
                        if processName.lower() in proc.name().lower():
                                # Monitor GPU
                                gpus = GPUtil.getGPUs()
                                load = gpus[0].load
                                last_load = 100.0
                                loaded = True
                                queueTime = 0
                                while(loaded):
                                        time.sleep(gpu_check_freq)
                                        # every gpu_chech_freq seconds
                                        queueTime += gpu_check_freq
                                        if (last_load > load):
                                                load = gpus[0].load
                                                last_load = load
                                        # every gpu_review_time seconds
                                        if (queueTime >= gpu_review_time):
                                                print('GPU idle too long. ')

                                return load
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
        #return False