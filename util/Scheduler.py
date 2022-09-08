class Scheduler:

    def __init__(self, watchdir, processname, parser):
        self.parser = parser
        self.watchdir = watchdir
        self.processname = processname

    def _check_file_count(self):
        from util.utilities import file_in_directory
        files = file_in_directory(self.watchdir)
        return len(files)

    def _check_if_process_running(self):
        '''Check if there are any running process that contains the given name processName.
        Iterate over the all the running process'''
        print('Checking if rendering is running...')
        import psutil
        for proc in psutil.process_iter():
                try:
                        # Check if process name contains the given name string.
                        if self.processname.lower() in proc.name().lower():
                                return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
        return False

    def _setup_rendering(self):
        '''Setup whole rendering'''
        print('Setup rendering...')
        from util.utilities import file_in_directory
        files = file_in_directory(self.watchdir)
        for file in files:
            self.parser.rewrite_frame_range(self.watchdir + "/" + file)

    def start(self):
        while(True):
            # Check if there are files to schedule and break if not
            if self._check_file_count()==0:
                print("There are no bat files to schedule.")
                break            
            # Setup rendering
            self._setup_rendering()
            break
            # Monitor the rendering
            # monitorProcess()
