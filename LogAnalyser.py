import re
import csv
import os
import time
#import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib import rc
import glob, xlwt
import pandas as pd
#import xlsxwriter
import tkinter
from tkinter import filedialog
import os



#rc('mathtext', default='regular')


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


def reformRSSI(s):
    s=clear_between(s,"[DEBUG] "," ")
    s=clear_between(s,",","Response [")
    s=s.replace("getChannel0RSSI=",",")
    s=s.replace(", getChannel1RSSI=",",")
    s=s.replace(", getChannel0CINR=",",")
    s=s.replace(", getChannel1CINR=",",")
    s=s.replace("]","")
    l=re.split(",",s)
    for i in range (1,5):
        l[i]=int(l[i])/2   
    return l

def reformWind(s):
    s=clear_between(s,"[DEBUG] "," ")
    time=find_between(s,"",",")
    wind=find_between(s,"Wind speed average ",",")
    gust=find_between(s,"momentary gust ",s.strip()[-1])
    l=[time,wind,gust]
    return l

def reformBMS(s):
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
    
    #Files creation:
    #RSSI/CINR csv file
    csvRSSI = open('Mobilicom.csv','w')
    rssi_wr = csv.writer(csvRSSI, dialect='excel',lineterminator='\n')
    csvRSSI.write("Time, RSSI 1, RSSI 2, CINR 1, CINR 2\n")

    #Metrology csv file
    csvMetrology = open('Metrology.csv','w')
    wr_metrology = csv.writer(csvMetrology, dialect='excel',lineterminator='\n')
    csvMetrology.write("Time, Wind, Gust\n")

    #BMS csv file
    csvBMS = open('BMS.csv','w')
    wr_bms = csv.writer(csvBMS, dialect='excel',lineterminator='\n')
    csvBMS.write("Time, SOC, SOH, Pack Volt, s1, s2, s3, s4 ,s5 ,s6, Difference, Temp.\n")
    
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
            if "NODE 192.168.131.242: MobilicomGetRssiCinrResponse" in line:
                csvline=reformRSSI(line)
                rssi_wr.writerow(csvline)
                csvcounter+=1
            elif "Wind speed average" in line:
                csvline=reformWind(line)
                wr_metrology.writerow(csvline)
                csvcounter+=1
            elif "ARM message arrived ArmMessage [bmsMessage=BMSPeriodicMessage" in line:
                csvline=reformBMS(line)
                wr_bms.writerow(csvline)
                csvcounter+=1
                
        datacounter+=len(contant)
        f.close()

    csvRSSI.close()    
    csvMetrology.close()
    csvBMS.close()


    writer = pd.ExcelWriter('Graphs.xlsx')
    for filename in glob.glob("*.csv"):
        df = pd.read_csv(filename)
        dot=filename.index(".")
        sheet_filename=filename[0:dot]
        df.to_excel(writer, sheet_name=sheet_filename)
        os.remove(filename)
    writer.save()

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

##    root = tkinter.Tk()
##    root.withdraw() #use to hide tkinter window
##    currdir = os.getcwd()
##    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
##    if len(tempdir) > 0:
##        print ("You chose " + tempdir)

    time.sleep(2)
##    print("Starting to plot the data\n"
##          "its going to take few seconds\n"
##          "------\n")

    

    



    
