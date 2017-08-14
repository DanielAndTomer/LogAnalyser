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
    time=find_between(s,"",",")
    wind=find_between(s,"Wind speed average ",",")
    gust=find_between(s,"momentary gust ",s.strip()[-1])
    l=[time,wind,gust]
    
    return l


if __name__ == "__main__":

    folderName=input("Insert the folder name:\n")
    logsList=os.listdir(folderName)
    
    cf = open('csvMetrology.csv','w')
    wr = csv.writer(cf, dialect='excel',lineterminator='\n')
    cf.write("Time, Wind, Gust\n")

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
            if "Wind speed average" in line:
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

    

    



    
