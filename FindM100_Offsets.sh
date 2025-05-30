#! /usr/bin/env bash
#
#    find centers of mom0 maps using NEMO's ccdblob
#
obsnums=97520,97521,97523,97524,97528,97529,97531,97532,97861,97863,97864,\
97870,97871,97993,97994,97999,98000,98006,98011,98012,98686,98687,\
98691,98692,98726,98727,98731,98732,98736,98737,98974,98975,99674,\
99675,99679,99680,99702,99703

pos=41,41
box=5


echo '# Computed with FindM100_Offsets.sh '
echo '#'
echo '# Obsnum   XMEAN    YMEAN'

export DEBUG=-1

for o in $(nemoinp $obsnums); do
    file=2021-S1-US-3/${o}/M100_${o}__0.mom0.fits
    if [ -e $file ]; then
	cen=$(fitsccd $file - | ccdblob - wcs=f pos=$pos box=$box | txtpar - p0=Center,1,2 p1=Center,1,3)
	echo "$o  $cen"
    else
	echo "# $o missing $file"
    fi
done
