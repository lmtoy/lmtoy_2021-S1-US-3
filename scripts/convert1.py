# convert the LMT pipeline cube from K to Jy/beam for the casaguide to work

#  casa:     execfile('convert1.py')
#  shell:    casa -c convert1.py

jyperk=3.2    
jyperk=2.7

#  need a subcube to avoid the noisy edges and just get the galaxy
#  we do need a few linefree channels in order for the casaguide to work
box1   = '17,17,72,72'
chans1 = '301~800'

importfits('M100_LMT.fits','im1',defaultaxes=True,defaultaxesvalues=['','','','I'],overwrite=True)
# @todo need an absolute RA-DEC box, not for this choice of the pipeline
#       equally so, the channel range is not robust, if we change the pipeline
imsubimage('im1','im2',box=box1,chans=chans1,overwrite=True)
imrebin('im2','im3',factor=[1,1,1,5],overwrite=True)
os.system('rm -rf im4')
immath('im3','evalexpr','im4','IM0*%g' % jyperk)
imhead('im4',mode='put',hdkey='BUNIT',hdvalue='Jy/beam')
os.system('rm -rf im5')
imtrans('im4',outfile='im5',order="012-3")
exportfits('im5','im5.fits',stokeslast=True, velocity=True, overwrite=True)
print('Flux: ',imstat('im5')['flux'][0], 'for Jy/K=',jyperk, 'box=',box1,'chans=',chans1)

# Flux:  3850.2201265533054 for Jy/K= 2.7 box= 17,17,72,72 chans= 301~800
