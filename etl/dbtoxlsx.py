#-------------------------------------------------------------------------------
# Name:        dbtoxlsx
# Purpose:     1. [read_config] : Read the config details from config2.txt to dictionary self.cfgdict
#              2. [sqltodf]     : Create dataframes ucdf1,ucdf2,ucdf3, and populate it from query in db
#              3. [do_formatting]     : Format the excel data 1) auto fit columns 2) apply styles 3) Set Tab color
#              4. [create_bar_chart]  : Create bar chart
#              5. [create_line_chart] : Create line chart
#              6. [dftoxls] : create the excel file with all the above formattings and charts
#
#  http://xlsxwriter.readthedocs.io/working_with_pandas.html
#
# Author:      Vidya Thotangare
# Created:     Apr 27, 2018
#-------------------------------------------------------------------------------

import csv
import os
import pandas as pd
import sqlalchemy
from datetime import datetime
import string

class dbtoxlsx:
    def __init__(self):
        self.cfgdict = {}
        self.read_config()
        self.ucdf1 = pd.DataFrame()
        self.ucdf2 = pd.DataFrame()
        self.ucdf3 = pd.DataFrame()


    def read_config(self):
        with open('config2.txt','rb') as cfgfile:
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
        print "User@DB : " + self.cfgdict["user"] + "@" + self.cfgdict["db"]
        print "------------------------------------------------------------------------------------------------"

        oracledb = sqlalchemy.create_engine (connstr)
        self.ucdf1 = pd.read_sql(self.cfgdict["qry1"], oracledb)
        self.ucdf2 = pd.read_sql(self.cfgdict["qry2"], oracledb)
        self.ucdf3 = pd.read_sql(self.cfgdict["qry3"], oracledb)

##        print "Total Records = " + str(len(self.ucdf3))
##        print self.ucdf3.columns
##        print self.ucdf3.columns.values


    def add_table(self, writer, sheetname, colnames, tablerange, stylename):
        workbook = writer.book
        worksheet = writer.sheets[sheetname]
        worksheet.add_table(tablerange, {'columns': colnames, 'autofilter': False, 'style': stylename})


    def do_formatting (self, df, sheetname, writer, tabcolor, stylename):
        # Formatting of the tables
        dataColumns = list(df.columns.values)

        headers = []
        for column in dataColumns:
            headers.append({'header': column})

        numRows = len(df) + 1
        numColumns = len(dataColumns) - 1
        tableRange = 'A1:' + string.ascii_uppercase[numColumns] + str(numRows)

        self.add_table(writer, sheetname, headers, tableRange, stylename)

        # Auto fit all the columns
        worksheet = writer.sheets[sheetname]
        worksheet.set_tab_color(tabcolor)
        for i, col in enumerate(df.columns):
            column_len = df[col].astype(str).str.len().max()
            column_len = max(column_len, len(col)) + 2
            worksheet.set_column(i, i, column_len)


    def create_bar_chart(self, df, sheetname, writer):
        workbook = writer.book
        worksheet = writer.sheets[sheetname]

        chart = workbook.add_chart({'type': 'column'})
        max_row = len(df)
        chart.add_series({
            'name' : "Employee Count",
            'categories':  [sheetname, 1, 1, max_row, 1],     # Sheetname, st row, st col, end row, end col
            'values':      [sheetname, 1, 2, max_row, 2],
            'fill':   {'color': '#4542f4'},
            'data_labels' : {'value' : True},
            'gap':        50,
        })

        chart.set_title({'name': "Employee Count per Department"})
        chart.set_x_axis({'name': 'Departments'})
        chart.set_y_axis({'name': 'Employee count', 'major_gridlines': {'visible': False}})
        chart.set_legend({'position': 'top'})
        worksheet.insert_chart('E4', chart) # position where the chart is placed


    def create_line_chart(self, df, sheetname, writer):
        workbook = writer.book
        worksheet = writer.sheets[sheetname]

        chart = workbook.add_chart({'type': 'line'})
        max_row = len(df)
        chart.add_series({
            'name' : "Employee Salary",
            'categories':  [sheetname, 1, 0, max_row, 0],     # Sheetname, st row, st col, end row, end col
            'values':      [sheetname, 1, 2, max_row, 2],
            'line':   {'color': '#f4b241'},
            'data_labels' : {'value' : True, 'font': {'rotation': 315}},
            'marker' : {'type' : 'diamond' , 'size': 8 , 'border' : {'color': 'blue'}, 'fill' : {'color': '#c141f4'} }
        })

        chart.set_title({'name': "Employee Salary Trend"})
        chart.set_x_axis({'name': 'Employee names'})
        chart.set_y_axis({'name': 'Salary', 'major_gridlines': {'visible': False}})
        chart.set_legend({'position': 'top'})
        chart.set_size({'x_scale': 2, 'y_scale': 2}) # increase the size of  chart
        worksheet.insert_chart('E2', chart ,{'x_offset': 25, 'y_offset': 10}) # offset is used to add chart in between cells


    def dftoxls(self):
        dt = datetime.now()
        dtstr = dt.strftime('%Y_%m_%d')

        xlsfile = os.path.join(os.getcwd() , self.cfgdict["xlsdir"], self.cfgdict["xlsfile"]) + "_" + dtstr + "_1.xlsx"
        os.remove(xlsfile) if os.path.exists(xlsfile) else None

        writer = pd.ExcelWriter(xlsfile, engine='xlsxwriter')

        self.ucdf1.to_excel(writer, sheet_name='Emp_Details', index=False)
        self.do_formatting(self.ucdf1, 'Emp_Details', writer, '#9BBB59', 'Table Style Medium 18')

        self.ucdf2.to_excel(writer, sheet_name='Dept_EmpCount', index=False)
        self.do_formatting(self.ucdf2, 'Dept_EmpCount', writer, '#8064A2', 'Table Style Medium 19')
        self.create_bar_chart(self.ucdf2,'Dept_EmpCount', writer)

        self.ucdf3.to_excel(writer, sheet_name='Emp_Sal', index=False)
        self.do_formatting(self.ucdf3, 'Emp_Sal', writer, '#4BACC6', 'Table Style Medium 20')
        self.create_line_chart(self.ucdf3,'Emp_Sal', writer)

        writer.save()


if __name__ == "__main__":
    dc = dbtoxlsx()

    #dc.printdict()
    dc.sqltodf()
    dc.dftoxls()


