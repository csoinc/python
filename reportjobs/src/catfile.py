__author__="oou01"
__date__ ="$20-Nov-2009 4:32:43 PM$"

f = open('/tmp/workfile', 'rb+')
i = 0

fname = 'C:/logfiles/epslog/20090915/LOG.FDC.CAD2.20090915003403'

with open(fname) as f:
    for line in f:
        print(line)
        idx = line.find("Merch ID")
        if idx <= 0:
            print("not find Merch ID")
        else: 
            print(line.find("Merch ID")) 
            i = i + 1
    
    print("Find total merch IDs ", i)
