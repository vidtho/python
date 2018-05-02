#-------------------------------------------------------------------------------
# Name:        GenReport
# Purpose:     1. [openfiles] : Read the csv file and store data to individual dataframes
#              2. [ca_linechrt]     : CPU capacity plot       from dlpx_prod_VMAX-analytics-cpu-aggregated.csv
#              3. [na_linechrt]     : Network capacity plot   from dlpx_prod_VMAX-analytics-network-aggregated.csv
#
# http://jonathansoma.com/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/
# https://matplotlib.org/users/tight_layout_guide.html
# http://jacksimpson.co/positioning-a-legend-outside-the-figure-with-matplotlib-and-python/
# https://elitedatascience.com/python-seaborn-tutorial
# http://ertycde1.blogspot.com/2012/04/python-matplotlibdatesdate2num.html
# https://stackoverflow.com/questions/33544637/add-future-dates-to-plot-for-trendline
# https://www.dataquest.io/blog/making-538-plots/
#
# Author:      Vidya Thotangare
# Created:     Apr 28, 2018
#
# Library needed :
# pandas, matplotlib, os,


#dlpx_prod_VMAX-analytics-cpu-aggregated.csv	    Capacity_CPU.jpg
#dlpx_prod_VMAX-analytics-cpu-raw.csv		        CPU.jpg
#dlpx_prod_VMAX-analytics-disk-aggregated.csv
#dlpx_prod_VMAX-analytics-disk-raw.csv		        DISK_Latency.jpg
#dlpx_prod_VMAX-analytics-disk-raw.csv		        DISK_IOPS.jpg
#dlpx_prod_VMAX-analytics-disk-raw.csv		        Disk_Throughput.jpg
#dlpx_prod_VMAX-analytics-iscsi-aggregated.csv
#dlpx_prod_VMAX-analytics-iscsi-raw.csv
#dlpx_prod_VMAX-analytics-network-aggregated.csv	Capacity_Network.png
#dlpx_prod_VMAX-analytics-network-raw.csv	        Network.jpg
#dlpx_prod_VMAX-analytics-nfs-aggregated.csv
#dlpx_prod_VMAX-analytics-nfs-raw.csv		        NFS_IOPS.png
#dlpx_prod_VMAX-analytics-nfs-raw.csv		        NFS_Latency.jpg
#dlpx_prod_VMAX-analytics-nfs-raw.csv		        NFS_Throughput.jpg
#dlpx_prod_VMAX-analytics-tcp-aggregated.csv
#dlpx_prod_VMAX-analytics-tcp-raw.csv
#??						                            Cache_Hit.jpg
#-------------------------------------------------------------------------------
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

class GenReport:
  def __init__(self):
         self.dfca = pd.DataFrame()
         self.dfcr = pd.DataFrame()
         self.dfda = pd.DataFrame()
         self.dfdr = pd.DataFrame()
         self.dfia = pd.DataFrame()
         self.dfir = pd.DataFrame()
         self.dfnta = pd.DataFrame()
         self.dfntr = pd.DataFrame()
         self.dfnfa = pd.DataFrame()
         self.dfnfr = pd.DataFrame()
         self.dfta = pd.DataFrame()
         self.dftr = pd.DataFrame()
         self.config_param()



  def openfiles(self):
    csvdir = os.path.join(os.getcwd() , 'csv')
    for root,dirs,files in os.walk(csvdir):
        for file in files:
           if file.endswith(".csv"):
               filename = os.path.join(csvdir, file)
               #print filename
               if file == "dlpx_prod_VMAX-analytics-cpu-aggregated.csv":
			       self.dfca = pd.read_csv (filename)
			       # print "Total Records = " + str(len(self.dfca))
			       # print self.dfca.columns
			       self.ca_linechrt(self.dfca)

               if file == "dlpx_prod_VMAX-analytics-network-aggregated.csv":
			       self.dfnta = pd.read_csv (filename)
			       # print "Total Records = " + str(len(self.dfnta))
			       # print self.dfnta.columns
			       self.nta_linechrt(self.dfnta)

               if file == "dlpx_prod_VMAX-analytics-nfs-raw.csv":
			       self.dfnfr = pd.read_csv (filename)
			       # print "Total Records = " + str(len(self.dfnfr))
			       # print self.dfnfr.columns
			       self.nfr_scatterchrt2(self.dfnfr)


  def config_param(self):
      self.xlab_fn = self.ylab_fn = self.title_fn = 'Arial'
      self.xlab_fs = self.ylab_fs = 12
      self.title_fs = 16
      self.xlab_fb = self.ylab_fb = self.title_fb = 'bold'
      self.xlab_fc = self.ylab_fc = self.title_fc = 'k'
      self.leg_loc = 'center left'
      self.pltblue = '#337499'
      self.pltred  = '#C14A4E'
      self.pltgrn  = '#99cc00'
      self.lnrblue = '#083d91'
      self.lnrred  = '#480404'


  def chrt_details(self, ax, plt, filename, xlab, ylab, title, rightmrg):
    plt.xticks(rotation=60)    # x-axis rotated to 45 deg
    plt.gca().yaxis.grid(True) # enable horizontal gridlines

    ax.set_xlabel(xlab, fontname=self.xlab_fn, fontsize=self.xlab_fs , fontweight=self.xlab_fb, color=self.xlab_fc)
    ax.set_ylabel(ylab, fontname=self.ylab_fn, fontsize=self.ylab_fs , fontweight=self.ylab_fb, color=self.ylab_fc)
    ax.set_title(title, fontname=self.title_fn, fontsize=self.title_fs , fontweight=self.title_fb, color=self.title_fc)

    ax.legend(loc=self.leg_loc, prop={'size':8}, bbox_to_anchor=(1, 0.5), frameon=False)

    plt.tight_layout(pad=3, h_pad=2, w_pad=2, rect=None) # Does not work well ...legend gets cut
    plt.subplots_adjust(left= 0.10, right = rightmrg) # New line to adjust above layout

    # plt.show() # See the output
    plt.savefig(filename)


  def add_trendlines(self, timeseries):
    self.x1, self.y1 = timeseries.index, timeseries
    self.x = self.x1.date.astype('O') # [New line] workaround for date conversion issue
    #rx2 = mdates.date2num(rx1) # gives error here looks like numpy.datetime64 not supported [64 bit issue]
    self.x2 = mdates.date2num(self.x)
    self.z = np.polyfit(self.x2,self.y1,1)
    self.p = np.poly1d(self.z)


  def ca_linechrt(self, df):
    plt.rcParams['figure.figsize'] = (10, 6)

    fig = plt.figure()
    ax = plt.subplot(111)
    df['#time'] = pd.to_datetime(df['#time']) # [New line] Date conversion:  [64 bit issue]

    ax.plot(df['#time'],df['utilization_min'],label='utilization_min', color=self.pltblue)
    ax.plot(df['#time'],df['utilization_max'],label='utilization_max', color=self.pltred)
    ax.plot(df['#time'],df['utilization_85pct'],label='utilization_85pct', color=self.pltgrn)

    self.chrt_details(ax, plt, "Capacity_CPU.png", "Date", "CPU", "85% CPU Variation for 1 week", 0.85)


  def nta_linechrt(self, df):
    plt.rcParams['figure.figsize'] = (10, 6)

    fig = plt.figure()
    ax = plt.subplot(111)
    df['#time'] = pd.to_datetime(df['#time']) # [New line] Date conversion:  [64 bit issue]

    ax.plot(df['#time'],df['outBytes_85pct']/1024/1024,label='85% Reads in MB', color=self.pltblue)
    ax.plot(df['#time'],df['inBytes_85pct']/1024/1024,label='85% Writes in MB', color=self.pltred)

    self.chrt_details(ax, plt, "Capacity_Network.png", "Date", "Throughput(MBPS)", "85% Network Throughput Variation for 1 week", 0.85)


  def nfr_scatterchrt2(self, df):
    pd.set_option('mode.chained_assignment', None)

    dfr = pd.DataFrame()
    dfw = pd.DataFrame()

    dfr = df[['#timestamp', 'ops_read']]
    dfr['#timestamp'] = pd.to_datetime(dfr['#timestamp'])
    sr = pd.Series (dfr['ops_read'].values, index = dfr['#timestamp'])


    dfw = df[['#timestamp', 'ops_write']]
    dfw['#timestamp'] = pd.to_datetime(dfw['#timestamp'])
    sw = pd.Series (dfw['ops_write'].values, index = dfw['#timestamp'])


    #== Plotting==============================================================
    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='ops_read', ms=1.5, ax=ax) ##0066a1
    sw.plot(figsize=(10,6), style = '.', color=self.pltred, label='ops_write', ms=2, ax=ax)

    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='read_linear' )

    self.add_trendlines(sw)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrred, label='write_linear' )

    self.chrt_details(ax, plt, "NFS_IOPS.png", "Date", "IOPS", "NFS Server operations per second", 0.90)



if __name__ == "__main__":
    gr = GenReport()
    gr.openfiles()