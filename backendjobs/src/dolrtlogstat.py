#!/usr/bin/python
#
__author__="Owen Ou"
__date__ ="$21-Dec-2009 4:32:43 PM$"

import os
import sys
from datetime import *
import shutil
import sendemail

src_pth = "/var/adm/logfiles/dol/dol"
rpt_pth = "/export/home/oou/dolrtlog/rpt"
scp_pth = "/export/home/oou/dolrtlog"

fname = "dol_real_time.log"
rpt_f_pre = "dolrt_stat"

#get the input data - yyyymmdd
if (len(sys.argv) > 1):
    in_timestamp = sys.argv[1]
    print ('input time', in_timestamp)
else:
    in_timestamp = raw_input("Please enter timestamp YYYYMMDD:")

out_timestamp = in_timestamp

in_fname = fname
out_fname = fname

if len(in_timestamp) == 0:
    out_timestamp_date = date.today()
    out_timestamp = out_timestamp_date.strftime("%Y%m%d")
else:
    in_fname = in_fname + "." + in_timestamp

out_fname = out_fname + "." + out_timestamp

print(in_fname + ":" + out_fname)

#copy log file to script folder
in_fullname = src_pth + '/' + in_fname
out_fullname = scp_pth + '/' + out_fname

shutil.copy2(in_fullname, out_fullname)

#open rpt files
try:
    more3s = rpt_pth + '/' + rpt_f_pre + '_' + out_timestamp + '_more3s.csv'
    rpt_more_3s = open(more3s, 'w')

except IOError:
    print "There was an error writting to ", more3s
    sys.exit()

try:
    less3s = rpt_pth + '/' + rpt_f_pre + '_' + out_timestamp + '_less3s.csv'
    rpt_less_3s = open(less3s, 'w')
except IOError:
    print "There was an error writting to ", less3s
    sys.exit()

#varibles
keys = ('Time','ReqUID','CorpNum','UserID','RTAction','TimeCost');
records = {'Time':'','ReqUID':'','CorpNum':'','UserID':'','RTAction':'','TimeCost':''}
users = {}

for x in keys:
    print x,
    rpt_more_3s.write(str(x))
    rpt_more_3s.write(',')
    rpt_less_3s.write(str(x))
    rpt_less_3s.write(',')

#for k, v in records.items():
#    rpt_more_3s.write(str(k))
#    rpt_more_3s.write(',')
#    rpt_less_3s.write(str(k))
#    rpt_less_3s.write(',')

rpt_more_3s.write('\n')
rpt_less_3s.write('\n')

#open log file to process
try:
    f = open(out_fullname, 'r')
except IOError:
    print "There was an error reading from ", out_fullname
    sys.exit()

#with open(out_fullname) as f:
for line in f:
    #print(line)
    if line.find('[FATAL]') >= 0:
        idx_trace_user = line.find('rt_trace_user[')
        idx_rt_action = line.find('rt_action[')
        idx_corp_num = line.find('corp_num=')
        idx_req_uid = line.find('reqUID[')
        idx_res_vo = line.find('resvo[')
        if int(idx_rt_action) != -1:
            records['Time'] = line[1:21]
            print ('time', line[1:21])
            idx_trace_session_id = line.find(']--trace_session_id')
            records['RTAction'] = line[idx_rt_action+10:idx_trace_session_id]
        if int(idx_req_uid) != -1:
            records['ReqUID'] = line[idx_req_uid+7:idx_res_vo-3]
        if int(idx_trace_user) != -1:
            trace_user_str = line[idx_trace_user:idx_rt_action-3]
            records['UserID'] = trace_user_str[14:]
        if int(idx_corp_num) != -1:
            corp_num_str = line[idx_corp_num:]
            idx_end = corp_num_str.find('}')
            records['CorpNum'] = corp_num_str[9:idx_end]
            users.setdefault(records.get('UserID','usr'),corp_num_str[9:idx_end])
        #print('find fatal')
    elif line.find('timespend :') >= 0:
        #print('find timespend')
        idx_timespend = line.find('timespend :')
        #print(idx_timespend)
        timespend_str = line[idx_timespend:]
        print('time_spend', timespend_str)
        timespend_num = float(timespend_str[12:])/1000
        records['TimeCost'] = timespend_num
        user_id = records.get('UserID')
        corp_num = users.get(user_id, '')
        print('corp_num', corp_num)
        if len(corp_num) > 0:
            records['CorpNum'] = corp_num

        if timespend_num >= 3.0:
            for x in keys:
                rpt_more_3s.write(str(records.get(x)))
                rpt_more_3s.write(',')
            #for k, v in records.items():
            #    rpt_more_3s.write(str(v))
            #    rpt_more_3s.write(',')
            rpt_more_3s.write('\n')
        else:
            for x in keys:
                rpt_less_3s.write(str(records.get(x)))
                rpt_less_3s.write(',')
            #for k, v in records.items():
            #    rpt_less_3s.write(str(v))
            #    rpt_less_3s.write(',')
            rpt_less_3s.write('\n')

        records = {'Time':'','ReqUID':'','CorpNum':'','UserID':'','RTAction':'','TimeCost':''}
     
    else:
        print('ignor line',(str(line)).strip())

f.close()

rpt_more_3s.close()
rpt_less_3s.close()

os.remove(out_fullname)
#shutil.rmtree(path, ignore_errors, onerror)

#email the reports
sendemail.sendemail(
    ["owen.ou@bmo.com"],
    "DOL RT Log Stat - " + out_timestamp,
    "Production DOL real-time performance statistic reports attached.",
    [more3s]
)
    