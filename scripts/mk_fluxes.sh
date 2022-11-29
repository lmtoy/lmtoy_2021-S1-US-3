#! /bin/bash
#
# M100_Feather_CO.image.mom0.pbcor.fits
# M100_combine_CO_cube.image.mom0.pbcor.fits
# M100_LMT.mom0.fits 

# @todo the ALMA maps don't have the same resolution as the LMT maps
#       4.6 x 2.9"   vs.  12.65"

fitsccd M100_Feather_CO.image.mom0.pbcor.fits - |\
 ccdellint - 0:200/3600:1/3600 150 40 180,263 tab=- rscale=3600 iscale=1/60.49 > M100_Feather.cumflux.tab

fitsccd M100_combine_CO_cube.image.mom0.pbcor.fits - |\
 ccdellint - 0:200/3600:1/3600 150 40 400,411 tab=- rscale=3600 iscale=1/60.49 > M100_combine.cumflux.tab




# cd ~/ALMA/DataComb/data/2021-S1-US-3/97520_99703
# Jy/K ~ 2.16 (= 1.41 / 0.65)
# 1.24 is the factor to bring it to ALMA
# @todo this is still the wrong conversion factor
fitsccd M100_LMT.mom0.fits  - |\
   ccdellint - 0:240/3600:10/3600 150 40 45,45 tab=- rscale=3600 iscale=1.41/0.55/0.65/6.0 >  M100_LMT.cumflux.tab



