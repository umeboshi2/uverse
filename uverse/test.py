import os
import sys
from datetime import datetime
import cPickle as Pickle
import time

import requests
from BeautifulSoup import BeautifulSoup as BS

picklefile = 'uverse.pickle'

interval = 10

class LogEntry(object):
    def __init__(self, ping_id, statustable, sendtime, recvtime, rstatuscode):
        pass

def is_state_good(span):
    if span['class'] == 'state-good':
        return True
    elif span['class'] == 'state-bad':
        return False
    else:
        raise RuntimeError, "Bad span %s" % span
    

def is_up(statustable):
    spans = statustable.findAll('span')
    if len(spans) != 2:
        raise RuntimeError, "Improper statustable"
    broadband_connection_span, line_up_span = spans
    return tuple(map(is_state_good, spans))


def get_bad_entries(blist):
    return [e for e in blist if is_up(e[1]) != (True, True)]

def mainloop():
    if not os.path.isfile(picklefile):
        emptylist = []
        with file(picklefile, 'w') as pf:
            Pickle.dump(emptylist, pf)
    biglist = Pickle.load(file(picklefile))
    ping_id = 0
    while ping_id < 100000:
        sendtime = datetime.now()
        r, statustable = get_status(home_url)
        recvtime = datetime.now()
        entry = (ping_id, statustable, sendtime, recvtime, r.status_code)
        biglist.append(entry)
        
        with file(picklefile, 'w') as pf:
            Pickle.dump(biglist, pf)
        time.sleep(interval)
        
        
biglist = Pickle.load(file(picklefile))

        
if __name__ == '__main__':
    bl = biglist
    
    
