#!/usr/bin/python
#

__author__="Owen Ou"
__date__ ="$03-May-2011 4:32:43 PM$"

import ftplib
import os

ftp = ftplib.FTP('ftp.canpages.ca', 'oyou','duochicai1')
#print "File List:"
#files = ftp.dir()
#print files

entries = ftp.nlst()
entries.sort()

print "ftp download %d files:" % len(entries)
for entry in entries:
    print "get file " + entry
    gFile = open("/home/ftp/" + entry, "wb")
    ftp.retrbinary('RETR %s' % entry, gFile.write)
    gFile.close()
    print "finished get file " + entry
    p = os.system("type \\home\\ftp\\" + entry)
    
ftp.quit()


#ftp.cwd("/")
#gFile = open("bermuda1.txt", "wb")
#ftp.retrbinary('RETR bermuda1.txt', gFile.write)
#ftp.retrlines('RETR bermuda1.txt', writeline)

#gFile.close()
#ftp.quit()

#gFile = open("bermuda1.txt", "r")
#buff = gFile.read()
#print buff
#gFile.close()

