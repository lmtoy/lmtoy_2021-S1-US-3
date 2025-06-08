# 2021-S1-US-3

PI summaries are in:   http://taps.lmtgtm.org/lmtslr/2021-S1-US-3/

This project observed M100 in the CO(1-0) 115 GHz transition using the
old single bank setup in the WARES correllator. One of the science
goals is to learn more about how important data combination of
interferometric and single dish is. A background example of this is
discussed in
https://casaguides.nrao.edu/index.php?title=M100_Band3_Combine_6.4

Given that ALMA is aiming (with ATLAST) for a 50m single dish, having
a combination between ALMA and LMT data seems appropriate.

https://github.com/teuben/lmtoy_2021-S1-US-3
## OBSNUM

A total of 46 science obsnum's were taken in the CO line (115.3
GHz). Eight (8) of those are labeled QAFAIL, i.e. bad. Summary of
all data taken is in lmtinfo.txt. The bad ones are also labeled with
QAFAIL in the comments.txt file.

We also have 36 pointing observations on RT-Vir, to check on the pointing.

Observations were taken in 7 nights in Spring 2022: April 5, 6, 7, 8, 27 and May 4, 17.
Links to http://lmtserver.astro.umass.edu/ShiftReports/ seem empty?


     Apr 5   begin, 2, end        http://lmtserver.astro.umass.edu/ShiftReports/Note-20220405.html
     Apr 6   begin, end           http://lmtserver.astro.umass.edu/ShiftReports/Note-20220406.html
     Apr 7   begin, 2, end, end   http://lmtserver.astro.umass.edu/ShiftReports/Note-20220407.html
     Apr 8   4, end, end          http://lmtserver.astro.umass.edu/ShiftReports/Note-20220408.html
     Apr 27  begin, 4, end        http://lmtserver.astro.umass.edu/ShiftReports/Note-20220427.html
     May 4   8xbegin, end         http://lmtserver.astro.umass.edu/ShiftReports/Note-20220504.html
     May 17  begin, 3, end        http://lmtserver.astro.umass.edu/ShiftReports/Note-20220517.html

       April                  May           
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  
                1  2   1  2  3  4  5  6  7  
 3  4  5  6  7  8  9   8  9 10 11 12 13 14  
10 11 12 13 14 15 16  15 16 17 18 19 20 21  
17 18 19 20 21 22 23  22 23 24 25 26 27 28  
24 25 26 27 28 29 30  29 30 31              
                                                                  

Current final RMS is down to just under 21 mK. Each dataset has a noise of around 100mK. 100/sqrt(46-7)=16,
so not quite as good as expected?  Some systematics we can work on? 

Beam 1 always bad, Beam 5 often, Beam 6 has some low pattern, might be useful to try leaving it
out for all?

Mark: I would recommend that we dump obsnums 98011 and 98012 from the combo. 
98011 shows a very sloppy distribution of Tdv values in the 7x7 pixel
area and a very low antenna temperatures.  98012 is very noisy with a
peak Tdv value 70% lower than most obsnums. 

### Creating the run files

A master script **mk_runs.my** contains all the global information on
which obsnums are good, which beams are good, etc.  You always will
need to re-run this script to create the SLpipeline *run* files,
normally through the `make runs` command.

The script also uses the (otherwise optional) `comments.txt` file,
where comments for the summary and deviant pipeline arguments specific
to an obsnum can be stored. These files should be edited by a user to
create a new "final" dataset. Any optional post-processing after the
pipeline will not be described here (but is of course recommended?).

This command creates the run files:

      make runs
	  
which creates the run files.

### Running the pipeline


With [SLURM](https://slurm.schedmd.com/documentation.html) this is the way on unity:

      sbatch_lmtoy2.sh 2021-S1-US-3.run1a 2021-S1-US-3.run1b 2021-S1-US-3.run2

On "lma" using gnu parallel instead this takes about 30 minutes to process all single obsnums
(run1) and a few combination maps (run2), or running them serially through bash takes a few hours.

## Science:

In the LMT+ALMA combination, the sole important parameter is the Jy/K factor, which we should
explain here.

### M100


## Files:


Description of the file that should be in this directory


      lmtinfo.txt               logfile from lmtinfo.py on all relevant science observations
      mk_runs.py                script to make the run files
      comments.txt              comments for the summary and optional pipeline parameters
      2021-S1-US-3.run1a        created by mk_runs.py
      2021-S1-US-3.run1b        created by mk_runs.py
      2021-S1-US-3.run2a        created by mk_runs.py
      2021-S1-US-3.run2b        created by mk_runs.py
      2021-S1-US-3/             (optional) directory with pipeline results, otherwise in $WORK_LMT

1. P R D R D P R D R D P                 01:15:04 04:27:29   8/8
2. P R D R D P				 05:07:45 06:32:44   0/4 - all bad (low elevation)
3. P R D R D P P P R D R D P P		 01:32:19 04:44:55   5/8 - 3 bad
4. R D P R D P P R D P R D P P		 01:18:20 04:20:57   6/8 - last 2 bad after all
5. P R D P R D P R D P R D P R D P	 22:45:35 03:22:22   10/10 
6. P P P P P P P P R D P       	 	 23:10:45 03:46:56   2/2
7. P R D P D C P P R D P		 23:04:34 01:41:04   6/6

P   =  1.5 min   pointing
R,D = 12.0 min   RA or DEC map

## Additional Pointing Corrections?

Since the emission in M100 is already fairly strong in a single obsnum, one experiment
to check on pointing is to make cross-correlation maps between them, and not rely on the
actual headers. Conceivably this could show some offsets, that could result in a
better aligned combination.  There was some indication there are some systematic offsets
in some of the data, so this could be a more advanced version, but there were also some
very unexplained facts about the cross-corr data.

As can be seen from the central pixel spectrum (the pipeline has this as the last figure)
there are very obvious cases where the skewness of the profile indicates a pointing offset.

Otherwise the effective beam for the ALMA+LMT combination is not the traditional 12", but more
like 13 or 14", which has some impact on fidelity and correctness of the combination.

From a higher resolution CO(2-1) alma image one can see the central velocity gradient
is about 20-25 km/s/arcsec.  At an assumed distance of 13.9 Mpc, this 30-40 km/s/kpc

The current gridding into 81 pixels means pixel 41 is the center M100 position (reference
pixel RA = 185.7288971   DEC = 15.82231045)

### Astrometry

summary:

- ALMA CO10 and CO21 agree well on the center:   12:22:54.934  +15:49:20.41   - error maybe 0.1"
- NED however is 1" off in RA and 2.5" in DEC:   12:22:54.8616 +15:49:17.886


####  CO-21 image:

peak at (0.4") pixel 271,265 - note reference pixel is 275.75,250.25 

```
ccdblob ngc4321_mom0.ccd 270,264  wcs=f clip=600 out=- | tabcomment - | tabnllsqfit - 1,2 3 fit=peak2d par=900,-100,-100,271,265
ccdblob ngc4321_mom0.ccd 270,264  wcs=f clip=500 out=- | tabcomment - | tabnllsqfit - 1,2 3 fit=gauss2d par=0,900,271,265,2


    ccdblob                               peak2d                           gauss2d

270.646 264.537     49  (peak=959)                                  270.11       263.88
270.344 264.188     32  clip=400
270.021 263.958     23  clip=500      270.12 0.07  263.82 0.07      270.10       263.81  
270.143 263.839     19  clip=600      270.06       263.88           270.06 0.05  263.85 0.05

xy2sky ngc4321_12m+7m+tp_co21_strict_mom0.fits 271.12  264.82 ->  12:22:54.934  +15:49:20.41 
                                               271.344 265.188    12:22:54.928  +15:49:20.56 
NED                                                               12:22:54.8616 +15:49:17.886     185.728590  15.821635
```

- conservatively the error is 0.1 pixels, or 0.04" in this case.
- an intensity weighted mean is prone to biases on a 7x7 grid.  clip= needs to be used to make it more symmetric

####  CO-10 image:

reference pixel 189.75 184.75, pixels are 0.6" - peak near 186,187

```
    ccdblob                                   peak2d                         gauss2d

185.238 186.083     49
185.394 186.045     21 clip=300000  185.40 0.06  186.17 0.06      185.41 0.04  186.18 0.05
 
185.529 186.234     16      350000
185.415 186.224     12      400000 

xy2sky ngc4321_12m+7m+tp_co10.fits 186.40 187.17       ->  12:22:54.939  +15:49:20.45
xy2sky data_2025/97520/M100_97520__0.mom0.fits 41 41       12:22:54.935  +15:49:20.32 
NED                                                        12:22:54.8616 +15:49:17.886     185.728590  15.821635
```

- conservatively the error is 0.06 pixels, or 0.03" in this case.
