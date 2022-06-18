import os
import sys
from time import time

WSL = 'WSL'


class OsSys:
    def __init__(self, boot_time):
        details = self.get_system_type()
        self.clear = details['clear']
        self.systype = details['systype']
        self.boot_time = boot_time
    
    def get_system_type(self):
        clear = 'clear'
    
        if sys.platform == 'win32':
            return {'clear': 'cls', 'systype': 'Windows'}
    
        if sys.platform == 'linux' and 'Microsoft' in os.uname()[2]:
            return {'clear': clear, 'systype': 'WSL'}
    
        if sys.platform == 'darwin':
            return {'clear': clear, 'systype': 'MacOS'}
    
        return {'clear': clear, 'systype': 'Linux'}

    def get_terminal_size(self):
        size = os.get_terminal_size()
        return {'width': size.columns, 'height': size.lines}

    def os_clear(self):
        os.system(self.clear)
        
    def get_uptime(self):
        time_diff = time() - self.boot_time
        uptime_hours = int(time_diff // 3600)
        uptime_minutes = int((time_diff // 60)) if uptime_hours < 1 else int((time_diff - (uptime_hours * 3600)) / 60)
        uptime_seconds = int(time_diff) if (uptime_minutes < 1 or (uptime_hours < 1 and uptime_minutes < 1)) else int(
            (time_diff - ((uptime_minutes * 60) + (uptime_hours * 3600))))
        return "Uptime em " + \
               self.systype + \
               (': 0' if uptime_hours < 10 else ': ') + \
               (str(uptime_hours) +
                (':0' if uptime_minutes < 10 else ':') +
                str(uptime_minutes) +
                (':0' if uptime_seconds < 10 else ':') +
                str(uptime_seconds))
