#!/usr/bin/python
#

__author__="Owen Ou"
__date__ ="$03-May-2011 4:32:43 PM$"

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os

def sendemail(to, subject, text, files=[], server="mx3.bmogc.net"):
    assert type(to)==list
    assert type(files)==list
    fro = "M&S Team <do_not_reply@details-online.com>"

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
            % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()

if __name__ == '__main__':
    sendemail(
        ["owen.ou@bmo.com"],
        "DOL RT Log Stat - 20091221",
        "Production DOL real-time performance statistic reports attached.",
        ["C:/temp/4383_code_01.xml","C:/temp/logo.png"]
    )

