import os
import csv
import sys
import statistics
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def slideMean(data, window, step):
    total = len(data)
    spots = list(range(1, total-window+1, step))
    result = [None] * len(spots)
    for i in range(0, len(spots)):
        result[i] = statistics.median(data[spots[i]-1:(spots[i]+window)])
    return result

def slideSlope(datax, datay, window, step):
    total = len(datax)
    spots = list(range(1, total-window+1, step))
    result = [None] * len(spots)
    for i in range(0, len(spots)):
        gradient, intercept, r_value, p_value, std_err = stats.linregress(datax[spots[i]-1:(spots[i]+window)],datay[spots[i]-1:(spots[i]+window)])
        temp = [intercept, gradient]
        result[i] = temp[1]
    return result

select_col = [
  "red"
  ,"blue"
  ,"darkgreen"
  ,"cyan"
  ,"cornflowerblue"
  ,"coral"
  ,"darkorange"
  ,"deeppink"
  ,"goldenrod"
  ,"lightsalmon"
  ,"red"
  ,"steelblue"
  ,"turquoise"
  ,"springgreen"
  ,"orchid"
  ,"blue"
  ,"darkslategray"
  ,"chartreuse"
  ,"darkred"
  ,"orangered"       
]
window = 51
step = 10

os.chdir("D://Eau_Physio_248mV")
savedir = "D://Eau_Physio_248mV"

angle = [
  "0Deg"
  ,"9Deg"
  ,"18Deg"
  ,"27Deg"
  ,"36Deg"
  ,"45Deg"
  ,"54Deg"
  ,"72Deg"
  ,"81Deg"
  ,"90Deg"
  ,"99Deg"
  ,"108Deg"
  ,"117Deg"
  ,"126Deg"
  ,"135Deg"
  ,"144Deg"
  ,"153Deg"
  ,"162Deg"
  ,"171Deg"
  ,"180Deg"
]
tension =[
   "2400"
  ,"2410"
  ,"2420"
  ,"2430"
  ,"2440"
  ,"2450"
  ,"2460"
  ,"2470"
  ,"2480"        
]
manip = [
          "Eau_Physio_248mV"
          ,"AIR A 2490mV"
          ,"1Abs_268mV_0mA_Ispec850"
          ,"2Abs_288mV_0mA_Ispec850"
          ,"4Abs_3260mV_9mA_Ispec850"
          ,"12Abs_3600mV_23mA_Ispec380"
          ,"24Abs_3600mV_23mA_Ispec200"
          ,"36Abs_3600mV_23mA_Ispec"
          ,"40Abs_3600mV_23mA_Ispec"        
]
prefix = [
          "/Eau_Physio_248mV_"
          ,"/AIR_"
          ,"/1Abs_268mV_0mA_Ispec850_"
          ,"/2Abs_288mV_0mA_Ispec850_"
          ,"/4Abs_3260mV_9mA_Ispec850_"
          ,"/12Abs_3600mV_23mA_Ispec380_"
          ,"/24Abs_3600mV_23mA_Ispec200_"
          ,"/36Abs_3600mV_23mA_Ispec_"
          ,"/40Abs_3600mV_23mA_Ispec_"
]
postfix = "_IntegT900E-3.LVM"

def convert(e):
    x = e[0]
    x = x.split("\t")
    x = map(toFloat, x)
    x = list(x)
    return x

def toFloat(e):
    if e == '':
        return 0
    return float(e) 

def extractV1(e):
    return e[0]

def extractV3(e):
    return e[2]

def input(i_angle, i_manip):
    file = "".join([savedir,"/",manip[i_manip],prefix[i_manip],angle[i_angle],postfix])
    print(file)
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data1 = list(reader)
    data1 = data1[24:]
    data1 = list(map(convert, data1))
    datax = list(map(extractV1, data1))
    datay = list(map(extractV3, data1))
    x = slideMean(datax, window, step)
    y = slideMean(datay, window, step)
    n = len(x)
    return [n,x,y]

pdf = PdfPages("".join([savedir,"/plots.pdf"]))

for i_manip in range(0, 9):   
    fig = plt.figure(figsize = (15,15))
    for i_angle in range(0, 20):
        data = input(i_angle, i_manip)
        n = data[0]
        w1 = data[1]
        spectre = data[2]
        plt.subplot(5,4,i_angle+1).set_ylim(0,1)
        plt.tight_layout()
        plt.plot(w1, spectre,'ro', color=select_col[i_angle], markersize=1)
        plt.grid()
        plt.title(angle[i_angle])        
    plt.suptitle(manip[i_manip], color="Black", y=1.05, fontsize="xx-large")
    fig.savefig(pdf, format="pdf", bbox_inches="tight")
    sys.stdout.flush() 
    
pdf.close()

