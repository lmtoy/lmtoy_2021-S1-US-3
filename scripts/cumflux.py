#! /usr/bin/env python
#
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
# plt.style.use("grayscale")

tab1 = 'M100_LMT.cumflux.tab'
data1 = np.loadtxt(tab1).T

tab2 = 'M100_combine.cumflux.tab'
data2 = np.loadtxt(tab2).T

tab3 = 'M100_Feather.cumflux.tab'
data3 = np.loadtxt(tab3).T

print(data1.shape)
#plt.figure(dpi=300,figsize=(20/2.54,20/2.54))
plt.figure()
plt.plot(data1[0],data1[5],label='12.65" LMT')
plt.plot(data2[0],data2[5],label='4.6x2.9" ALMA-7+12m')
plt.plot(data3[0],data3[5],label='4.6x2.9" ALMA-Feather')
#plt.step(data1[0],data1[2],label=tab1,where='mid')
#plt.scatter(data1[0],data1[2],label=tab1)
#plt.errorbar(data1[0],data1[2],data1[-1],label=tab1)
plt.xlabel('Radius [arcsec]')
plt.ylabel('Cumulative Flux [Jy.km/s]')
#plt.xlim([0,1])
#plt.ylim([0,1])
plt.title('M100 PA=150 INC=40')
plt.legend()
plt.savefig('cumflux.pdf')
plt.show()

#
print("Last LMT          ",data1[5][-1],'at radius ',data1[0][-1])
print("Last ALMA-feather ",data3[5][-1],'at radius ',data3[0][-1])
print("Last ALMA-combine ",data2[5][-1],'at radius ',data2[0][-1])
