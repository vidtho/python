#-------------------------------------------------------------------------------
# Name:        csvtodb
# Purpose:  Functions 1 and 2 for csv file ; Function 3 and 4 for pipe seperated file
#              1. [openfiles]   : Go to folder and read all .csv files one by one
#              2. [readfiles]   : read first line of csv file(column header) ;
#                                   Convert all the columns as list csvlst ;
#                                   save it as rows in dataframe orcldf
#                                   Load the dataframe to vid.vid_config
#              3. [opentxtfiles] : Go to network folder and
#                                   read pipe seperated files (.txt) mathing pattern in that directory
#                                   + exclude given files given in exlist
#              4. [readpipefiles]: open pipe file loop through the first line (column header) and break after that
#                                   Convert all the columns as list csvlst ;
#                                   save it as rows in dataframe orcldf + filename (2 columns)
#                                   Load the dataframe to vid.vid_config
#
# Author:      Vidya Thotangare
# Created:     Sep 3, 2017
#-------------------------------------------------------------------------------

import csv
import os
import pandas as pd
import sqlalchemy

def openfiles():
    csvdir = os.path.join(os.getcwd() , 'csvfiles')
    for root,dirs,files in os.walk(csvdir):
        for file in files:
           if file.endswith(".csv"):
               filename = os.path.join(csvdir, file)
               print filename
               readfiles(filename)


def readfiles(pfilename):
    csvdf = pd.read_csv (pfilename, nrows=1).columns

    csvlst = list(csvdf)
    orcldf = pd.DataFrame({'csvcols':csvlst})
    #print orcldf
    print "Total Records Loaded = " + str(len(orcldf))

    oracledb = sqlalchemy.create_engine ('oracle://vid:vid@viddb')
    orcldf.to_sql('vid_config', oracledb, if_exists='append', index = False)


def opentxtfiles():
    csvdir = os.path.join('\\\\cryptology.net\\DevApplication\\viddb' , 'vid')
    pattern = "emp"
    exlist = ["retired_emp.txt", "left_emp.txt", "dead_emp.txt"]


    for root,dirs,files in os.walk(csvdir):
        for file in files:
            if file not in exlist:
               if file.endswith(".txt") and pattern in file:
                  filename = os.path.join(csvdir, file)
                  print filename
                  readpipefiles(filename,file)


def readpipefiles(pfilename,pfile):
    with open(pfilename,'rb') as csvfile:
       linereader = csv.reader(csvfile, delimiter='|')
       for row in linereader:
           #print row
           csvlst = row
           break
    orcldf = pd.DataFrame({'csvcols':csvlst})
    orcldf['csvfile'] = pfile
    #print orcldf
    print "Total Records Loaded = " + str(len(orcldf))

    oracledb = sqlalchemy.create_engine ('oracle://vid:vid@viddb')
    orcldf.to_sql('vid_config', oracledb, if_exists='append', index = False)

#===========================================================
#openfiles()
opentxtfiles()