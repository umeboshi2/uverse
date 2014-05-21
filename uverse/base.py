import os
import sys
from datetime import datetime
import cPickle as Pickle
import time

import requests
from BeautifulSoup import BeautifulSoup as BS

gateway_ip = '192.168.1.254'

home_url = 'http://%s/cgi-bin/home.ha' % gateway_ip

picklefile = 'uverse.pickle'

interval = 10

class LogEntry(object):
    def __init__(self, ping_id, statustable, sendtime, recvtime, rstatuscode):
        pass
    
def get_status(url):
    now = datetime.now()
    r = requests.get(url)
    statustable = None
    if r.ok:
        b = BS(r.content)
        statustable = b.find('table')
    return r, statustable


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
        
        
        
        
if __name__ == '__main__':
    mainloop()
    
