# 2021-S1-US-3

This project observed M100 in the CO(1-0) 115 GHz transition using the
old single bank setup in the WARES correllator. One of the science
goals is to learn more about how important data combination of
interferometric and single dish is. A background example of this is
discussed in
https://casaguides.nrao.edu/index.php?title=M100_Band3_Combine_6.4

Given that ALMA is aiming (with ATLAST) for a 50m single dish, having
a combination between ALMA and LMT data seems appropriate.

## OBSNUM

A total of 46 science obsnum's were taken in the CO line (115.3
GHz). Eight (8) of those are labeled QAFAIL, i.e. bad. Summary of
all data taken is in lmtinfo.txt. The bad ones are also labeled with
QAFAIL in the comments.txt file.

We also have 36 pointing observations on RT-Vir, to check on the pointing.

Observations were taken in 7 nights in Spring 2022: April 5, 6, 7, 8, 27 and May 4, 17.

     Apr 5   begin, 2, end
     Apr 6   begin, end
     Apr 7   begin, 2, end, end
     Apr 8   4, end, end
     Apr 27  begin, 4, end
     May 4   8xbegin, end
     May 17  begin, 3, end

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
4. R D P R D P P R D P R D P P		 01:18:20 04:20:57   8/8
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

Otherwise the effective beam for the ALMA+LMT combination is not the traditional 12", but more
like 13 or 14", which has some impact on fidelity and correctness of the combination.

