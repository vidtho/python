#-------------------------------------------------------------------------------
# Name:        file _plots.py
# Purpose:
#
# Author:      vthotang
#
# Created:     05/10/2017
# Copyright:   (c) vthotang 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import csv

def load_data1():
    x = []
    y = []

    with open('example.txt') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(int(row[0]))
            y.append(int(row[1]))

    plt.plot(x,y,label='loaded from file')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck it out')

    plt.legend(loc='upper left')
    plt.show() # Figure 1

def load_data2():
    x = []
    y = []

    with open('example.txt') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(int(row[0]))
            y.append(int(row[1]))



    plt.plot(x,y,label='loaded from file')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck it out')

    plt.legend(loc='upper left')
    plt.show() # Figure 1


if __name__ == "__main__":
   load_data1()
##   load_data2()
