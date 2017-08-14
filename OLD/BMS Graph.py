import re
import csv
import os
import time

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
    time=find_between(s,""," ")
    soc=find_between(s,"c=",",")
    soh=find_between(s,"h=",",")
    packVolt=find_between(s,"packVolt=",",")
    l=[time,soc,soh,packVolt]
    cells=find_between(s,"cellsVolts=[","]")
    cells=cells.split(",")
    l.extend(cells)
    for i in range(0,6):
        cells[i]=int(cells[i])
    diff=max(cells)-min(cells)
    l.append(diff)
    temp=find_between(s,"temperature=",",")
    l.append(temp)
    return l


if __name__ == "__main__":

    folderName=input("Insert the folder name:\n")
    logsList=os.listdir(folderName)
    
    cf = open('csvBMS.csv','w')
    wr = csv.writer(cf, dialect='excel',lineterminator='\n')
    cf.write("Time, SOC, SOH, Pack Volt, s1, s2, s3, s4 ,s5 ,s6, Difference, Temp.\n")

    print("------\n"+
        "In progress !\n"+
        str(len(logsList))+
        " log files was imported\n"+
        "it going to take around "+
        str(round(5/16*len(logsList),2))+
        " seconds")
    csvcounter=0
    datacounter=0
    startAll=time.time()
    
    for file in logsList:
        
        #deals with each log file
        path=folderName+"\\"+file
        f = open(path,'r')
        contant = f.read().split("\n")
        
        for line in contant:
            #deals each line in log file
            if "ARM message arrived ArmMessage [bmsMessage=BMSPeriodicMessage" in line:
                csvline=reformLine(line)
                wr.writerow(csvline)
                csvcounter+=1
                
        datacounter+=len(contant)
        f.close()
        
    cf.close()

    dur=time.time()-startAll
    print("------\n"+
          "DONE!\n"+
          str(len(logsList))+
          " files was imported\n"+
          "witch contains "+
          str(datacounter)+
          " lines, \n"+
          str(csvcounter)+
          " lines has parsed\n"+
          "It took " + str(round(dur,2)) +
          " sec to complete the task\n"+
          "------\n")
    time.sleep(2)
##    print("Starting to plot the data\n"
##          "its going to take few seconds\n"
##          "------\n")

    

    



    
