from ftplib import FTP_TLS
import os

def grabFile():

    filename = 'log-log.2017-08-16-155047.log.gz'

    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp.quit()
    localfile.close()

##ftp = FTP('logs.autodrones4biz.com')
##ftp.login(user='airouser', passwd = 'Thru6102Pxj')
##
##ftp.cwd('/airobotics/qa8/ds/01/ds_server/logs')

ftp =  FTP_TLS( 'logs.autodrones4biz.com' )
ftp.login( 'airouser' , 'Thru6102Pxj')
ftp.prot_p()
ftp.cwd('/airobotics/qa8/ds/01/ds_server/logs')



grabFile()

ftp.close()
