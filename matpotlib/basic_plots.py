#-------------------------------------------------------------------------------
# Name:        basic _plots.py
# Purpose:
#
# Author:      vthotang
#
# Created:     05/10/2017
# Copyright:   (c) vthotang 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import matplotlib.pyplot as plt

def linechrt():
    x1 = [1,2,3]
    y1 = [5,7,4]

    x2 = [1,2,3]
    y2 = [10,14,12]

    plt.plot(x1,y1,label='First Line')
    plt.plot(x2,y2, label = 'Second Line')

    plt.xlabel('Plot Number')
    plt.ylabel('Important Var')
    plt.title('Interesting Graph\nCheck it out')

    plt.legend(loc='upper left')
    plt.show() # Figure 1


def barchrt():
    x = [2,4,6,8,10]
    y = [6,7,8,2,4]

    x2 = [1,3,5,7,9]
    y2 = [7,8,2,4,2]

    plt.bar(x, y, label='Bars1', color='#6600cc' )
    plt.bar(x2, y2, label='Bars2', color = '#ffcc00')


    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck it out')

    plt.legend(loc='upper right')
    plt.show() # Figure 2


def histogram():
    population_ages = [22,44,62,45,21,35,33,55,66,75,12,25,34,47,56,64,73,84,91,111,89,70,65,52,47,32,21]
    ids = [x for x in range(len(population_ages))]
    bins = [0,10,20,30,40,50,60,70,80,90,100,110]

    #plt.bar(ids, population_ages, label='Bars1', color='c') # Figure 3
    plt.hist(population_ages, bins, histtype='bar', rwidth=0.8, label='Distribution of\npopulation ages', color='r') # put all the populations in their respective bins like "mode" [mean , median, mode]

    plt.xlabel('ids')
    plt.ylabel('population ages')
    plt.title('Interesting Graph\nCheck it out')

    plt.legend(loc='upper right')
    plt.show() # Figure 4


def scatterplot():
    # marker options : https://matplotlib.org/api/markers_api.html

    x = [1,2,3,4,5,6,7,8]
    y = [6,7,8,2,4,2,4,5]
    z = [5,6,4,3,2,3,1,2]
    p = [3,5,9,8,6,4,2,1]

    plt.scatter(x,y,label ='red', color='r', marker ='*', s = 30 )  # marker: star
    plt.scatter(x,z,label ='purple', color='#6600cc', marker ='o', s = 30 ) # marker: circle
    plt.scatter(x,p,label ='cyan', color='c', marker ='^', s = 30 ) # marker: triange

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck it out')

    plt.legend(loc='upper right')
    plt.show() # Figure 5

def stackplot():
    days =  [1,2,3,4,5]
    sleep = [7,8,10,6,9]
    eat =   [1,2,1,2,3]
    work =  [8,9,10,7,5]
    play =  [2,3,1,2,3]


    plt.plot([],[],color='m', label = 'Sleep', linewidth = 5) # scatter plot does not allow label so this is a workaround
    plt.plot([],[],color='c', label = 'Eat' , linewidth = 5)
    plt.plot([],[],color='#ffbf00', label = 'Work' , linewidth = 5)
    plt.plot([],[],color='#4000ff', label = 'Play' , linewidth = 5)

    plt.stackplot(days, sleep, eat, work, play, colors = ['m','c','#ffbf00','#4000ff'])


    plt.xlabel('days')
    plt.ylabel('activities')
    plt.title('Interesting Graph\nCheck it out')

    plt.legend(loc='lower right')
    plt.show() # Figure 6

def piechart():

    slices = [7,2,5,13]
    activities = ['sleep', 'eat' , 'work', 'play']
    cols = ['m','c','#ffbf00','#4000ff']

    plt.pie(slices,
            labels = activities,
            colors = cols,
            startangle = 90,            # starting angle 90
            shadow = True,              # add shadow
            explode = (0, 0.1, 0, 0),   # take out the eat piece
            autopct = '%1.1f%%')        # add percent to pie

    plt.title('Activities performed in 5 days')

    plt.show() # Figure 7

if __name__ == "__main__":
##    linechrt()
##    barchrt()
##    histogram()
##    scatterplot()
##    stackplot()
    piechart()
