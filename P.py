import os
import csv
import sys
import math
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

rootdir = f"{os.getcwd()}"
os.chdir(f"{os.getcwd()}\Mesures dans l'air")
savedir = f"{os.getcwd()}"


def convert(e):
    x = '.'.join(e)
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
    return e[1]

def input(d, f):
    file = "".join([savedir,"/",d, "/", f])
    print(file)
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data1 = list(reader)
    data1 = data1[24:-1]
    data1 = list(map(convert, data1))
    datax = list(map(extractV1, data1))
    datay = list(map(extractV3, data1))
    x = slideMean(datax, window, step)
    y = slideMean(datay, window, step)
    n = len(x)
    return [n,x,y]

pdf = PdfPages("".join([rootdir,"/plots.pdf"]))

dirs = ['Abs0_xxmA_0Deg_5010µs']
#for dir in os.listdir():
#    if Path(f"{os.getcwd()}/{dir}").is_dir():
#        dirs.append(dir)

dirs.sort(key=len)
disp_max:int = 25
for dir in dirs:   
    
    files = []
    for (root,folder,file) in os.walk(dir):
        files = file
        break
    
    files.sort(key=len)
    for i, file in enumerate(files):
        if i % disp_max is 0:
            if i is not 0:
                plt.suptitle(dir, color="Black", y=1.05, fontsize="xx-large")
                fig.savefig(pdf, format="pdf", bbox_inches="tight")
            fig = plt.figure(figsize = (15,15))
                        
        
        data = input(dir, file)
        n = data[0]
        w1 = data[1]
        spectre = data[2]
        
        lg = len(files)
        y = 5
        x = math.ceil(lg/y)
        
        plt.subplot(5, 5, (i % disp_max)+1).set_ylim(0,3)
        plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=1.0)
        plt.plot(w1, spectre,'ro', color=select_col[i % len(select_col)], markersize=1)
        plt.grid()
        plt.title(file)  
        
        if i is len(files)-1:
            plt.suptitle(dir, color="Black", y=1.05, fontsize="xx-large")
            fig.savefig(pdf, format="pdf", bbox_inches="tight")
            
    sys.stdout.flush() 
    
pdf.close()
