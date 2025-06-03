from astropy.io import fits
import numpy as np
from reproject import reproject_interp
from scipy.stats import skew
from astropy import wcs
from astropy.convolution import Gaussian2DKernel,convolve_fft
from astropy.modeling import models,fitting
from astropy.coordinates import SkyCoord
#import misc
import matplotlib.pylab as plt
import math

vrange=[1400,1700]  # km/s range of nucleus emission
#obsnums=['97520_99703']     # LMT list of obsnums
#obsnums=['97871']     # LMT list of obsnums
obsnums=[97520]
#obsnums=[97520,97521,97523,97524,97528,97529,97531,97532,
#97861,97863,97864,97870,97871,97993,97994,97999,98000,
#98006,98011,98012,98686,98687,98691,98692,98726,98727,
#98731,98732,98736,98737,98974,98975,99674,
#99675,99679,99680,99702,99703]

alma,almaH=fits.getdata('./ngc4321/ngc4321_12m+7m+tp_co21.fits',header=True)
#X,Y,V=misc.getaxes(almaH)
NV,NY,NX=alma.shape
V=almaH['CRVAL3']+(np.arange(nv)-(almaH['CRPIX3']-1))*almaH['CDELT3']
V=V/1000
VDX=np.where((V >= vrange[0]) & (V <= vrange[1]))
alma_m0=np.sum(alma[VDX],axis=0)*abs(almaH['CDELT3'])/1000
#alma_m0=np.sum(alma[VDX[0],alma_peak[1]-32:alma_peak[1]+33,alma_peak[0]-32:alma_peak[0]+33],axis=0)*abs(almaH['CDELT3'])

alma_m0H=almaH.copy()
alma_m0H['NAXIS']=2
alma_m0H.remove('NAXIS3')
alma_m0H.remove('CTYPE3')
alma_m0H.remove('CDELT3')
alma_m0H.remove('CRVAL3')
alma_m0H.remove('CRPIX3')
alma_m0H.remove('CUNIT3')
alma_m0H.remove('PC3_1')
alma_m0H.remove('PC3_2')
alma_m0H.remove('PC1_3')
alma_m0H.remove('PC2_3')
alma_m0H.remove('PC3_3')
alma_wcs=wcs.WCS(alma_m0H)

Index=np.argmax(alma_m0[263-3:263+4,270-3:270+4])
tmp=np.unravel_index(Index,(7,7))
IYMAX=263-3+tmp[0]
IXMAX=270-3+tmp[1]
print(IXMAX,IYMAX)
xalma,yalma=alma_wcs.wcs_pix2world(np.array([IXMAX]),np.array([IYMAX]),0)
C0=SkyCoord(xalma,yalma,frame='icrs',unit='degree')
print(C0)

tb_max=alma[:,IYMAX,IXMAX]
# Convolve to LMT beam of 12"
dtmp=math.sqrt(12**2-(almaH['BMAJ']*almaH['BMIN'])*(3600**2))
dtmp=dtmp/2.35  # convert from FWHM to dispersion
dtmp=dtmp/abs(almaH['CDELT1'])/3600   # units of pixels
kernel=Gaussian2DKernel(dtmp)
ATMP=np.zeros((NV,65,65))    
for K in range(NV):
   ATMP[K]=convolve_fft(alma[K,IYMAX-32:IYMAX+33,IXMAX-32:IXMAX+33],kernel)
tb_convolve_max=ATMP[:,32,32]


FP=open('m100_lmt_offsets.txt','w')
FP.write('Obsnum     XMEAN     YMEAN      DX      DY       xmean_g       ymean_g       DX_g       DY_g\n')   
for obs in obsnums:
   lmtfile='./Data/M100_'+str(obs)+'__0.fits'
   print('Reading lmtfile ',lmtfile)
   lmt,lmtH=fits.getdata(lmtfile,header=True)
   lmt=lmt/0.6      # Beam efficiency
   nv,ny,nx=lmt.shape
#   x,y,v=misc.getaxes(lmtH)
   v=lmtH['CRVAL3']+(np.arange(nv)-(lmtH['CRPIX3']-1))*lmtH['CDELT3']
   v=v/1000
   vdx=np.where((v >= vrange[0]) & (v <= vrange[1]))
   lmt_m0=np.sum(lmt[vdx],axis=0)*abs(lmtH['CDELT3'])/1000

   lmt_m0H=lmtH.copy()
   lmt_m0H['NAXIS']=2
   lmt_m0H.remove('NAXIS3')
   lmt_m0H.remove('CTYPE3')
   lmt_m0H.remove('CDELT3')
   lmt_m0H.remove('CRVAL3')
   lmt_m0H.remove('CRPIX3')
   lmt_m0H.remove('CUNIT3')
   lmt_wcs=wcs.WCS(lmt_m0H)
   
# Find offsets by fitting data to 2D gaussian
   PeakIndex=np.argmax(lmt_m0[40-3:40+4,40-3:40+4])
   tmp=np.unravel_index(PeakIndex,(7,7))
   ixmax=40-3+tmp[1]
   iymax=40-3+tmp[0]
   xpix=np.arange(ixmax-3,ixmax+4,1)
   ypix=np.arange(iymax-3,iymax+4,1)
   XPIX,YPIX=np.meshgrid(np.arange(ixmax-3,ixmax+4,1),np.arange(iymax-3,iymax+4,1))
   XMEAN=round(np.sum(XPIX*lmt_m0[YPIX,XPIX])/np.sum(lmt_m0[YPIX,XPIX]),2)
   YMEAN=round(np.sum(YPIX*lmt_m0[YPIX,XPIX])/np.sum(lmt_m0[YPIX,XPIX]),2)
   print('Centroids: ',XMEAN,YMEAN)

   Z=lmt_m0[iymax-3:iymax+4,ixmax-3:ixmax+4].copy()
   guess_amplitude=lmt_m0[iymax,ixmax]
   guess_xmean=ixmax
   guess_ymean=iymax
   guess_x_stddev=1
   guess_y_stddev=1
   guess_theta=0
   GUESS=models.Gaussian2D(amplitude=guess_amplitude,x_mean=guess_xmean,y_mean=guess_ymean, x_stddev=guess_x_stddev,y_stddev=guess_y_stddev,theta=guess_theta)
   fit = fitting.LevMarLSQFitter()
   fitted_model = fit(GUESS, XPIX, YPIX, Z)
   print(fitted_model)
   print(fitted_model.amplitude.value)

   xlmt,ylmt=lmt_wcs.wcs_pix2world(np.array([XMEAN]),np.array([YMEAN]),0)
   C1=SkyCoord(xlmt,ylmt,frame='icrs',unit='degree')
   print(C1)
# Show gauss 2d fit

   xlmt_g,ylmt_g=lmt_wcs.wcs_pix2world(np.array([fitted_model.x_mean.value]),np.array([fitted_model.y_mean.value]),0)
   C2=SkyCoord(xlmt_g,ylmt_g,frame='icrs',unit='degree')
   deltax_g=(C2.icrs.ra.deg - C0.icrs.ra.deg)*3600
   deltay_g=(C2.icrs.dec.deg - C0.icrs.dec.deg)*3600

   str0=str('%s     %4.2f      %4.2f       %4.2f   %4.2f      %4.2f    %4.2f     %4.2f     %4.2f\n' % (obs,XMEAN,YMEAN,deltax,deltay,fitted_model.x_mean.value,fitted_model.y_mean.value,deltax_g,deltay_g))
   FP.write(str0)
   print(str0)

   plt.figure(100)
   plt.clf()
   plt.imshow(lmt_m0,origin='lower',vmin=0,vmax=fitted_model.amplitude.value)
   plt.xlim(XPIX[0,0],XPIX[-1,-1])
   plt.ylim(YPIX[0,0],YPIX[-1,-1])
   GFIT=fitted_model(XPIX,YPIX)
   levs=np.array([0.5,0.6,0.7,0.8,0.9,1])*fitted_model.amplitude.value
   plt.contour(XPIX,YPIX,GFIT,levs,colors='w')
   plt.plot(np.array([XMEAN]),np.array([YMEAN]),'ko')
   plt.plot(np.array([fitted_model.x_mean.value]),np.array([fitted_model.y_mean.value]),'ro')
   plt.title(str('Obsnum: %d' % obs),loc='left')


FP.close()
