import os
import csv
import sys
import statistics
import numpy as np
from scipy import stats
from pathlib import Path
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

os.chdir(f"{os.getcwd()}\Eau_Physio_248mV")
savedir = f"{os.getcwd()}"


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

def input(d, f):
    file = "".join([savedir,"/",d, "/", f])
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

dirs = []
for dir in os.listdir():
    if Path(f"{os.getcwd()}/{dir}").is_dir():
        dirs.append(dir)

for dir in dirs:   
    fig = plt.figure(figsize = (20,20))
    files = []
    for (root,folder,file) in os.walk(dir):
        files = file
        break
    for i, file in enumerate(files):
        data = input(dir, file)
        n = data[0]
        w1 = data[1]
        spectre = data[2]
        plt.subplot(5,5,i+1).set_ylim(0,1)
        plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=1.0)
        plt.plot(w1, spectre,'ro', color=select_col[i], markersize=1)
        plt.grid()
        plt.title(file[:20]+"...")        
    plt.suptitle(dir, color="Black", y=1.05, fontsize="xx-large")
    fig.savefig(pdf, format="pdf", bbox_inches="tight")
    sys.stdout.flush() 
    
pdf.close()
