#!/usr/bin/python
#

__author__="Owen Ou"
__date__ ="$03-May-2011 4:32:43 PM$"

import ftplib
import os

ftp = ftplib.FTP('ftp.canpages.ca', 'oyou','duochicai1')

entries = ftp.nlst()
entries.sort()

print "ftp & unzip %d files:" % len(entries)
for entry in entries:
    print "get file " + entry
    gFile = open("/home/ftp/" + entry, "wb")
    ftp.retrbinary('RETR %s' % entry, gFile.write)
    gFile.close()
    print "unzip file " + entry
    p = os.system("type \\home\\ftp\\" + entry)
    #p = os.system("type \\home\\ftp\\" + entry)
    print "successful on ftp & unzip file " + entry
    
ftp.quit()
