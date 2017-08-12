import re
import csv
import os


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def clear_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        toclear = s[start:end]
        toclear=first+toclear+last
        s=s.replace(toclear,"")
        return s
    except ValueError:
        print ("[ERROR]: Sub string didn't found")


def reformLine(s):
    s=clear_between(s,"[DEBUG] "," ")
    s=clear_between(s,",","Response [")
    s=s.replace("getChannel0RSSI=",",")
    s=s.replace(", getChannel1RSSI=",",")
    s=s.replace(", getChannel0CINR=",",")
    s=s.replace(", getChannel1CINR=",",")
    s=s.replace("]","\n")
    return s

if __name__ == "__main__":

    folderName=input("Insert the folder name:\n")
    logsList=os.listdir(folderName)
    
    cf = open('csvFile.csv','w')
    cf.write("Time, RSSI 1, RSSI 2, CINR 1, CINR 2\n")
    
    for file in logsList:
        #path=os.path.join(folderName, file)
        path=folderName+"\\"+file
        print (path)
        f = open(path,'r')
        contant = f.read().split("\n")
        for line in contant:
            if "NODE 192.168.131.242: MobilicomGetRssiCinrResponse" in line:
                csvline=reformLine(line)
                print (csvline)
                cf.write(csvline)
                        
        
        f.close()
        
    cf.close()



    
