#!/usr/bin/env python -u
# -*- coding: utf-8 -*-
# vim:et
# ---------------------------------------------------------------------------
# nasledie-grabber.py
# Author: Maxim Dubinin (sim@gis-lab.info)
# About: Grab Moskomnasledie data from http://dkn.mos.ru/contacts/register-of-objects-of-cultural-heritage/memorial/ data on cultural heritage. Simply iterate through id and get contents.
# Created: 20:05 05.02.2014
# Usage example: python nasledie-grabber.py 1 100001
# ---------------------------------------------------------------------------

#import urllib
import urllib2
from httplib import BadStatusLine,IncompleteRead
import socket
import sys
import os
import datetime
import time

def console_out(text):
    global time_prev
    time_current = datetime.datetime.now()
    timestamp = time_current.strftime('%Y-%m-%d %H:%M:%S')
    
    if time_prev == 0:
        timedif = ""
    else:
        timedif = str((time_current - time_prev).seconds)
    
    spaces = " "*(4 - len(timedif))
    print(timestamp + "  " + timedif + spaces + text)
    time_prev = time_current
    
def download_org(link,id):
    global time_prev
    numtries = 5
    timeoutvalue = 40
    timeinterval = 1
    
    for i in range(1,numtries+1):
        i = str(i)
        try:
            #user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)"
            #headers = { 'User-Agent' : user_agent }
            #values = {'name' : 'John Doe','language' : 'Python' }
            #data = urllib.urlencode(values)
            #req = urllib2.Request(link, data, headers)
            #u = urllib2.urlopen(req)
            u = urllib2.urlopen(link, timeout = timeoutvalue)
        except BadStatusLine:
            console_out('BadStatusLine for ID:' + id + '.' + ' Attempt: ' + i)
            success = False
            time.sleep(3)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                console_out('We failed to reach a server for ID:' + id + ' Reason: ' + str(e.reason) + '.' + ' Attempt: ' + i)
            elif hasattr(e, 'code'):
                console_out('The server couldn\'t fulfill the request for ID: ' + id + ' Error code: ' + str(e.code) + '.' + ' Attempt: ' + i)
            success = False
            time.sleep(3)
        except socket.timeout, e:
            console_out('Connection timed out on urlopen() for ID: ' + id + '.' + ' Attempt: ' + i)
            success = False
            time.sleep(3)
        else:
            f = open("data/" + id + ".html","wb")
            try:
                r = u.read()
            except socket.timeout, e:
                console_out('Connection timed out on socket.read() for ID: ' + id + '.' + ' Attempt: ' + i)
                success = False
                u.close()
                time.sleep(3)
            except IncompleteRead:
                console_out('Incomplete read on socket.read() for ID: ' + id + '.' + ' Attempt: ' + i)
                success = False
                u.close()
                time.sleep(3)
            else:
                f.write(r)
                f.close()
                console_out("Listing " + id + " downloaded")
                success = True
                break
    
    time_current = datetime.datetime.now()
    time_diff = (time_current - time_prev).seconds
    if time_diff < timeinterval:
        time.sleep(timeinterval - time_diff)
    return success
    
if __name__ == '__main__':
    args = sys.argv[1:]
    start_id = int(args[0])
    end_id = int(args[1]) + 1
    
    time_prev = 0
    
    f_errors = open("errors" + "_" + str(start_id) + "_" + str(end_id) + ".csv","a")
    if not os.path.exists("data"): os.makedirs("data")
       
    for id in range(start_id,end_id):
        id = str(id)
        link = "http://dkn.mos.ru/contacts/register-of-objects-of-cultural-heritage/memorial/" + id + "/"
        
        if not os.path.exists("data/" + id + ".html") or os.stat("data/" + id + ".html")[6]==0:
            success = download_org(link,id)
            if success == False:
                f_errors.write(id + "," + link + ", unavailable" + "\n")
        else:
            console_out("Listing for id " + id + " already exists")
        
    f_errors.close()
