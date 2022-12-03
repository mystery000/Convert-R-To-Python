#####################################################################################
#
#      Lecture automatique, traitement et tracé matriciel des spectres visibles
#             Développé par Patrick Perré, CentraleSupélec, Juin 2022
#
#####################################################################################

rm(list=ls())
library(latex2exp)

slideMean <- function(data, window, step){
  total <- length(data)
  spots <- seq(from=1, to=(total-window), by=step)
  result <- vector(length = length(spots))
  for(i in 1:length(spots)){
    #result[i] <- mean(data[spots[i]:(spots[i]+window)])
    result[i] <- median(data[spots[i]:(spots[i]+window)])
  }
  return(result)
}

slideSlope <- function(datax, datay, window, step){
  total <- length(datax)
  spots <- seq(from=1, to=(total-window), by=step)
  result <- vector(length = length(spots))
  for(i in 1:length(spots)){
    temp <-coef(lm(datay[spots[i]:(spots[i]+window)] ~ datax[spots[i]:(spots[i]+window)]))
    result[i] <-temp[2]
  }
  return(result)
}

select_col = c(
  "red"
  ,"blue"
  ,"darkgreen"
  ,"cyan3"
  ,"cornflowerblue"
  ,"coral3"
  ,"darkorange1"
  ,"deeppink3"
  ,"goldenrod2"
  ,"lightsalmon2"
  ,"red4"
  ,"steelblue"
  ,"turquoise2"
  ,"springgreen4"
  ,"orchid3"
  ,"navyblue"
  ,"darkslategray3"
  ,"chartreuse4"
  ,"darkred"
  ,"orangered"
)

window = 51
step = 10

setwd("C:/Users/hiya/Documents/R To Python")
savedir = "C:/Users/hiya/Documents/R To Python"

angle = c(
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
)

tension = c(
  "2400"
  ,"2410"
  ,"2420"
  ,"2430"
  ,"2440"
  ,"2450"
  ,"2460"
  ,"2470"
  ,"2480"
)

manip = c(
          "0.2Abs_2520mV_0mA_Ispec850"
          ,"Eau_Physio_248mV"
          ,"AIR_2490mV"
          ,"1Abs_268mV_0mA_Ispec850"
          ,"2Abs_288mV_0mA_Ispec850"
          ,"4Abs_3260mV_9mA_Ispec850"
          ,"12Abs_3600mV_23mA_Ispec380"
          ,"24Abs_3600mV_23mA_Ispec200"
          ,"36Abs_3600mV_23mA_Ispec"
          ,"40Abs_3600mV_23mA_Ispec")

prefix = c(
          "/0.2Abs_2520mV_0mA_Ispec850_"
          ,"/Eau_Physio_248mV_"
          ,"/AIR_"
          ,"/1Abs_268mV_0mA_Ispec850_"
          ,"/2Abs_288mV_0mA_Ispec850_"
          ,"/4Abs_3260mV_9mA_Ispec850_"
          ,"/12Abs_3600mV_23mA_Ispec380_"
          ,"/24Abs_3600mV_23mA_Ispec200_"
          ,"/36Abs_3600mV_23mA_Ispec_"
          ,"/40Abs_3600mV_23mA_Ispec_")

postfix = "_IntegT900E-3.LVM"

input = function(i_angle, i_manip){
  file = paste(savedir,"/",manip[i_manip],prefix[i_manip],angle[i_angle],postfix, sep = "")
  data1 = read.table(file,header=FALSE,skip = 24, sep = "\t")
  x = slideMean(data1$V1, window, step)
  y = slideMean(data1$V3, window, step)
  n = length(x)
  return(c(n,x,y))
}

for (i_manip in (1:1)){
  
  cairo_pdf(paste(savedir,manip[i_manip],".pdf", sep = ""), onefile=FALSE, height=8, width=8, pointsize=12)
  
  par(mfrow=c(5,4))
  
  par(oma=c(0,0,3,0))
  
  par(mar=c(2,2,1,1)+0.1)

  for (i_angle in (1:20)){
    data = input(i_angle, i_manip)
    n = data[1]
    wl = data[2:(1+n)]
    spectre = data[(2+n):(2*n+1)]
    plot(wl, spectre, type = 'p', cex =0.2, ylim = c(0,1),col = select_col[i_angle], main = angle[i_angle])
    grid()
  }
  mtext(manip[i_manip], side=3, line=1, cex=1.2, col="Black", outer=TRUE)  
  dev.off()
}