#-------------------------------------------------------------------------------
# Name:        dbtocsv
# Purpose:     1. [read_config] : Read the config details from config.txt to dictionary self.cfgdict
#              2. [sqltodf]     : Create dataframe avlndf and populate it from query in db
#              3. [dftocsv]     : Create csv file from dataframe avlndf
#
# Author:      Vidya Thotangare
# Created:     Oct 04, 2017
#-------------------------------------------------------------------------------

import csv
import os
import pandas as pd
import sqlalchemy
from datetime import datetime

class dbtocsv:
    def __init__(self):
        self.cfgdict = {}
        self.read_config()
        self.avlndf = pd.DataFrame()



    def read_config(self):
        with open('config.txt','rb') as cfgfile:
            for line in cfgfile:
                line = line.split('#', 1)[0]                    # Skip comment lines
                line = line.strip()                             # Remove empty lines
                if line:
                    (key, val) = line.split(':')
                    self.cfgdict[key.strip()] = val.strip()     # trim the spaces for key and value


    def printdict(self):
        for keys,values in self.cfgdict.items():
            if keys == "pwd":
                print keys + " : x1x2x3x4x5"
            else:
                print keys + " : " + values



    def sqltodf(self):
        connstr = "oracle://%s:%s@%s"%(self.cfgdict["user"], self.cfgdict["pwd"], self.cfgdict["db"] )

        print "------------------------------------------------------------------------------------------------"
        print "DB Query  : " + self.cfgdict["qry"]
        print "User@DB : " + self.cfgdict["user"] + "@" + self.cfgdict["db"]
        print "------------------------------------------------------------------------------------------------"

        oracledb = sqlalchemy.create_engine (connstr)
        self.avlndf = pd.read_sql(self.cfgdict["qry"], oracledb)

        print "Total Records = " + str(len(self.avlndf))
        print self.avlndf.columns


    def dftocsv(self):
        dt = datetime.now()
        dtstr = dt.strftime('%Y_%m_%d')

        csvfile1 = os.path.join(os.getcwd() , self.cfgdict["csvdir"], self.cfgdict["csvfile"]) + "_" + dtstr + "_1.csv"
        csvfile2 = os.path.join(os.getcwd() , self.cfgdict["csvdir"], self.cfgdict["csvfile"]) + "_" + dtstr + "_2.csv"

        self.avlndf.to_csv(csvfile1, index=False )
        self.avlndf.to_csv(csvfile2, index=False, quoting=csv.QUOTE_ALL, date_format='%Y-%m-%d')  # add quotes to all fields and  date format as yyyy-mm-dd



if __name__ == "__main__":
    dc = dbtocsv()

##    dc.printdict()
    dc.sqltodf()
    dc.dftocsv()


