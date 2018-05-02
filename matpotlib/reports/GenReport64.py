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
# https://www.youtube.com/watch?v=uSB8UBrbMfk
# https://chrisalbon.com/python/data_wrangling/pandas_join_merge_dataframe/
#
# Author:      Vidya Thotangare
# Created:     Apr 28, 2018
#
# Library needed :
# pandas, matplotlib, os,
#-------------------------------------------------------------------------------
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from scipy.interpolate import spline

class GenReport64:
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
         self.disk = self.nfs = 0
         pd.set_option('mode.chained_assignment', None)



  def openfiles(self):
    csvdir = os.path.join(os.getcwd() , 'csv')
    for root,dirs,files in os.walk(csvdir):
        for file in files:
           if file.endswith(".csv"):
               filename = os.path.join(csvdir, file)
               if file == "dlpx_prod_VMAX-analytics-cpu-aggregated.csv":
			       self.dfca = pd.read_csv (filename)
			       self.capacity_cpu(self.dfca)

               if file == "dlpx_prod_VMAX-analytics-network-aggregated.csv":
			       self.dfnta = pd.read_csv (filename)
			       self.capacity_network(self.dfnta)

               if file == "dlpx_prod_VMAX-analytics-nfs-raw.csv":
			       self.dfnfr = pd.read_csv (filename)
			       self.nfs_iops(self.dfnfr)
			       self.nfs_latency(self.dfnfr)
			       self.nfs_throughput(self.dfnfr)
			       self.nfs = 1

               if file == "dlpx_prod_VMAX-analytics-network-raw.csv":
			       self.dfntr = pd.read_csv (filename)
			       self.network_throughput(self.dfntr)

               if file == "dlpx_prod_VMAX-analytics-disk-raw.csv":
			       self.dfdr = pd.read_csv (filename)
			       self.disk_latency(self.dfdr)
			       self.disk_iops(self.dfdr)
			       self.disk_throughput(self.dfdr)
			       self.disk = 1

               if file == "dlpx_prod_VMAX-analytics-cpu-raw.csv":
			       self.dfcr = pd.read_csv (filename)
			       self.cpu_raw(self.dfcr)

    if (self.disk == 1) and (self.nfs == 1) :
       filename = os.path.join(csvdir, 'cache_hit_ratio.csv')
       self.cache_hit_ratio(self.dfdr, self.dfnfr, filename)


  def config_param(self):
      self.xlab_fn = self.ylab_fn = self.title_fn = 'Arial'
      self.xlab_fs = self.ylab_fs = 12
      self.title_fs = 16
      self.xlab_fb = self.ylab_fb = self.title_fb = 'bold'
      self.xlab_fc = self.ylab_fc = self.title_fc = 'k'
      self.leg_loc = 'center left'
      self.pltblue = '#0066CC'
      self.pltred  = '#C14A4E'
      self.pltgrn  = '#99cc00'
      self.lnrblue = '#000080'
      self.lnrred  = '#800080'


  def chrt_details(self, ax, plt, filename, xlab, ylab, title, rightmrg=0.85):
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


  def create_series(self, df, calc=1):
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
    df[df.columns[1]] = df[df.columns[1]] / calc
    sr = pd.Series (df[df.columns[1]].values, index = df[df.columns[0]])
    # print sr[0:5]
    return sr


  def capacity_cpu(self, df):
    plt.rcParams['figure.figsize'] = (10, 6)

    fig = plt.figure()
    ax = plt.subplot(111)
    df['#time'] = pd.to_datetime(df['#time']) # [New line] Date conversion:  [64 bit issue]
    ax.plot(df['#time'],df['utilization_min'],label='utilization_min', color=self.pltblue)
    ax.plot(df['#time'],df['utilization_max'],label='utilization_max', color=self.pltred)
    ax.plot(df['#time'],df['utilization_85pct'],label='utilization_85pct', color=self.pltgrn)

    self.chrt_details(ax, plt, "Capacity_CPU.png", "Date", "CPU", "85% CPU Variation for 1 week")


  def capacity_network(self, df):
    plt.rcParams['figure.figsize'] = (10, 6)

    fig = plt.figure()
    ax = plt.subplot(111)
    df['#time'] = pd.to_datetime(df['#time']) # [New line] Date conversion:  [64 bit issue]
    ax.plot(df['#time'],df['outBytes_85pct']/1024/1024,label='85% Reads in MB', color=self.pltblue)
    ax.plot(df['#time'],df['inBytes_85pct']/1024/1024,label='85% Writes in MB', color=self.pltred)

    self.chrt_details(ax, plt, "Capacity_Network.png", "Date", "Throughput(MBPS)", "85% Network Throughput Variation for 1 week")


  def nfs_iops(self, df):
    sr = self.create_series(df[['#timestamp', 'ops_read']])
    sw = self.create_series(df[['#timestamp', 'ops_write']])

    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='ops_read', ms=1.5, ax=ax)
    sw.plot(figsize=(10,6), style = '.', color=self.pltred, label='ops_write', ms=2, ax=ax)

    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(ops_read)' )
    self.add_trendlines(sw)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrred, label='Linear(ops_write' )

    self.chrt_details(ax, plt, "NFS_IOPS.png", "Date", "IOPS", "NFS Server operations per second")


  def nfs_latency(self, df):
    sr = self.create_series(df[['#timestamp', 'read_latency']])
    sw = self.create_series(df[['#timestamp', 'write_latency']])

    # sr = sr.ix[sr <= 40]
    # sw = sw.ix[sw <= 40]

    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)
    plt.ylim(0,40)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='read_latency', ms=1.5, ax=ax)
    sw.plot(figsize=(10,6), style = '.', color=self.pltred, label='write_latency', ms=2, ax=ax)

    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(read_latency)' )
    self.add_trendlines(sw)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrred, label='Linear(write_latency)' )

    self.chrt_details(ax, plt, "NFS_Latency.png", "Date", "Latency(ms)", "Internal NFS Latency")


  def nfs_throughput(self, df):
    sr = self.create_series(df[['#timestamp', 'read_throughput']])
    sw = self.create_series(df[['#timestamp', 'write_throughput']])

    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='read_throughput', ms=1.5, ax=ax)
    sw.plot(figsize=(10,6), style = '.', color=self.pltred, label='write_throughput', ms=2, ax=ax)

    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(read_throughput)' )


##    x_smooth = np.linspace(self.x2.min(), self.x2.max(), 300)
##    y_smooth = spline(self.x2,self.p(self.x2),x_smooth)
##    plt.plot(self.x1,y_smooth)


    self.add_trendlines(sw)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrred, label='Linear(write_throughput)' )

    self.chrt_details(ax, plt, "NFS_Throughput.png", "Date", "Throughput(MBPS)", "NFS Throughput from the Delphix Engine to the Targets")


  def network_throughput(self, df):
    inMB = float(1024*1024)
    sr = self.create_series(df[['#timestamp', 'inBytes']], inMB )
    sw = self.create_series(df[['#timestamp', 'outBytes']], inMB)

    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='Reads in MB', ms=1.5, ax=ax)
    sw.plot(figsize=(10,6), style = '.', color=self.pltred, label='Writes in MB', ms=2, ax=ax)

    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(Reads in MB)' )
    self.add_trendlines(sw)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrred, label='Linear(Writes in MB)' )

    self.chrt_details(ax, plt, "Network.png", "Date", "Network Throughput(MBPS)", "Total VM Network Throughput from the Delphix Engine to all Sources/Targets")


  def disk_latency(self, df):
    sr = self.create_series(df[['#timestamp', 'read_latency']])
    sw = self.create_series(df[['#timestamp', 'write_latency']])

    sr = sr.ix[sr <= 20]
    sw = sw.ix[sw <= 20]

    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)
    # plt.ylim(0,25)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='read_latency', ms=1.5, ax=ax)
    sw.plot(figsize=(10,6), style = '.', color=self.pltred, label='write_latency', ms=2, ax=ax)

    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(read_latency)' )
    self.add_trendlines(sw)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrred, label='Linear(write_latency)' )

    self.chrt_details(ax, plt, "DISK_Latency.png", "Date", "Latency(ms)", "Internal Disk Latency")


  def disk_iops(self, df):
    sr = self.create_series(df[['#timestamp', 'ops_read']])
    sw = self.create_series(df[['#timestamp', 'ops_write']])

    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='ops_read', ms=1.5, ax=ax)
    sw.plot(figsize=(10,6), style = '.', color=self.pltred, label='ops_write', ms=2, ax=ax)

    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(ops_read)' )
    self.add_trendlines(sw)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrred, label='Linear(ops_write' )

    self.chrt_details(ax, plt, "DISK_IOPS.png", "Date", "Disk IOPS", "Disk IOPS from the Delphix Engine to the Storage")

  def disk_throughput(self, df):
    sr = self.create_series(df[['#timestamp', 'read_throughput']])
    sw = self.create_series(df[['#timestamp', 'write_throughput']])

    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='read_throughput', ms=1.5, ax=ax)
    sw.plot(figsize=(10,6), style = '.', color=self.pltred, label='write_throughput', ms=2, ax=ax)

    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(read_throughput)' )
    self.add_trendlines(sw)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrred, label='Linear(write_throughput)' )

    self.chrt_details(ax, plt, "Disk_Throughput.png", "Date", "Throughput(MBPS)", "Disk Throughput from the Delphix Engine to the Storage")


  def cpu_raw(self, df):
    sr = self.create_series(df[['#timestamp', 'util']])
    plt.rcParams['figure.figsize'] = (6, 6)

    fig = plt.figure()
    ax = plt.subplot(111)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='util', ms=1.5, ax=ax)
    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(util)' )

    self.chrt_details(ax, plt, "CPU.png", "Date", "CPU", "CPU Utilization")

  def cache_hit_ratio (self, dfd, dfn, filename):
    dfdsk = pd.DataFrame()
    dfnfs = pd.DataFrame()
    dfchr = pd.DataFrame()

    dfdsk = dfd[['#timestamp', 'read_throughput']]
    dfnfs = dfn[['#timestamp', 'read_throughput']]

    dfchr = pd.merge(dfdsk, dfnfs, on='#timestamp', how='inner', suffixes=('_dsk', '_nfs'))
    dfchr['cache_hit_ratio'] = 100 - ((dfchr['read_throughput_dsk']*100)/dfchr['read_throughput_nfs'])

    dfchr = dfchr[(dfchr['read_throughput_dsk'] > 0) & (dfchr['read_throughput_nfs'] > 0) & (dfchr['cache_hit_ratio'] > 0)]
    dfchr.to_csv(filename)

    # Plotting============================================================
    sr = self.create_series(dfchr[['#timestamp', 'cache_hit_ratio']])
    plt.rcParams['figure.figsize'] = (10, 6)

    fig = plt.figure()
    ax = plt.subplot(111)

    sr.plot(figsize=(10,6), style = '.', color=self.pltblue, label='Cache Hit Ratio', ms=1.5, ax=ax)
    self.add_trendlines(sr)
    plt.plot(self.x1, self.p(self.x2), ls='-',color=self.lnrblue, label='Linear(Cache Hit Ratio)' )

    self.chrt_details(ax, plt, "Cache_Hit.png", "Date", "% Cash Hit", "Cache Hit Ratio for NFS Reads", 0.80)



if __name__ == "__main__":
    gr = GenReport64()
    gr.openfiles()