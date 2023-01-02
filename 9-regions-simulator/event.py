import numpy as np

class Event:
    
    def __init__(self, time, type, source, dest):
        self.time = time
        self.type = type
        self.source = source
        self.dest = dest
        
    def __lt__(self, other):
        return self.time < other.time
        
    def __repr__(self) -> str:
        # return 'Event(time:{!r}'.format(self.time)
        return 'Event(time:{!r}, type:{!r}, s:{!r}, d:{!r})'.format(self.time, self.type, self.source, self.dest)