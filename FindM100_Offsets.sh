#! /usr/bin/env bash
#
#    find centers of mom0 maps using NEMO's ccdblob
#
#    disturbing:
# ./FindM100_Offsets.sh box=4 > tab4
# ./FindM100_Offsets.sh box=3 > tab3
# paste tab3 tab4 | tabplot - 3 7 41 43 41 43 point=2,0.1 layout=diag.layout
#    this is not a 1:1 relationship

# the 39 good obsnums for M100
obsnums=97520,97521,97523,97524,97528,97529,97531,97532,97861,97863,97864,\
97870,97871,97993,97994,97999,98000,98006,98011,98012,98686,98687,\
98691,98692,98726,98727,98731,98732,98736,98737,98974,98975,99674,\
99675,99679,99680,99702,99703

# 
pos=41,41    # 97520 41.4367 41.2316 42.116
pos=40,40    # 97520 41.2916 40.871 42.116
box=5
link=2021-S1-US-3
link=data_2023
link=data_2025
clip=20

#       parse the commandline
for arg in "$@"; do
    export "$arg"
done


echo '# Computed with FindM100_Offsets.sh '
echo "#    pos=$pos box=$box clip=$clip link=$link"
echo '#'
echo '# Obsnum   XMEAN    YMEAN    Xgauss Ygauss     Xpeak Ypeak'
echo '#          pixel    pixel ...'

export DEBUG=-1

for o in $(nemoinp $obsnums); do
    file=$link/${o}/M100_${o}__0.mom0.fits
    if [ -e $file ]; then
	tmp=tmp_$o.tab
	cen1="cen1"
	cen2="cen2"
	c=""
	# cen1:   a blob fit using moments of inertia, using box= and clip= to select
	# cen1=$(fitsccd $file - | ccdblob - wcs=f pos=$pos box=$box clip=$clip | txtpar - p0=Center,1,2 p1=Center,1,3 p2=DataMinMax,1,3)
	cen1=$(fitsccd $file - | ccdblob - wcs=f pos=$pos box=$box clip=$clip | txtpar - p0=Center,1,2 p1=Center,1,3)
	if [ $? != 0 ] ; then  c="#" ; fi

	# cen2: a 2D gaussian fit, but using ccdblob to select the same points as used in the MOI method
	#       making sure pixel 1 based coordinates returned
	fitsccd $file - | ccdblob - wcs=f pos=$pos box=$box clip=$clip out=- | tabcomment - > $tmp
	# cen2=$(tabnllsqfit tmp_$o.tab  1,2 3 fit=gauss2d par=1,40,$pos,2|txtpar - %1,%2,%3+1,%4+1,%5,%6,%7 p0=a=,1,2 p1=b=,1,2 p2=c=,1,2 p3=d=,1,2 p4=e=,1,2 p5=c=,1,3 p6=d=,1,3)
	cen2=$(tabnllsqfit $tmp  1,2 3 fit=gauss2d par=1,30,$pos,1|txtpar - p0=c=,1,2 p1=d=,1,2)	
	if [ $? != 0 ] ; then  c="#" ; fi
	#cen3=$(tabnllsqfit tmp_$o.tab  1,2 3 fit=peak2d par=40,-1,-1,$pos|txtpar - p0=a=,1,2 p1=b=,1,2 p2=c=,1,2 p3=d=,1,2 p4=e=,1,2)
	cen3=$(tabnllsqfit $tmp  1,2 3 fit=peak2d par=30,-1,-1,$pos|txtpar - p0=d=,1,2 p1=e=,1,2)
	# rm -f $tmp
    else
	echo "# $o missing $file"
    fi
    echo "$c $o $cen1    $cen2    $cen3"
done
