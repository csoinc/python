#!/usr/bin/python
#

__author__="Owen Ou"
__date__ ="$03-May-2011 4:32:43 PM$"

import os
from datetime import *

log_path = "c:/logfiles/epslog/20090915"
filename = "C:/logfiles/epslog/20090915/LOG.ach.20090915003403"
reportname = "C:/logfiles/epslog/report/achtest.csv"

#print(os.listdir(log_path))
def parse(filename):
    format = "%Y%m%d %H:%M:%S"
    rpt_file = open(reportname, 'a')
    counter = 0
    record = {'process':'', 'records':'', 'cost':''}

    with open(filename) as f:
        for line in f:
            if line.find("ACH Settlement Program START") > 0:
                record['process'] = "ACH"
                dtstr = line[0:17]
                print(dtstr)
                logstr = line[17:]
                print(logstr)
                dt = datetime.strptime(dtstr, format)
                print(dt)
                start_time = dt
            if line.find("order id") > 0:
                counter = counter + 1
            if line.find("Closing created FILE = LOG.ach") > 0:
                dtstr = line[0:17]
                print(dtstr)
                dt = datetime.strptime(dtstr, format)
                print(dt)
                end_time = dt
                record['records'] = counter
                record['cost'] = end_time - start_time    
    for k, v in record.items():
        print(k, v)
        rpt_file.write(str(v))
        rpt_file.write(',')
    rpt_file.write('\n')

for f in os.listdir(log_path):
    if os.path.isfile(os.path.join(log_path, f)):
        print(f)
        if f.find("ach") > 0:
            parse(os.path.join(log_path, f))


##import fileinput
##for line in fileinput.input():
##    print(line)