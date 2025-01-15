# 2021-S1-US-3

This project observed M100 in the CO(1-0) 115 GHz transition. One of the science goals is to learn
more about how important data combination of interferometric and single dish is. A background
example of this is discussed in https://casaguides.nrao.edu/index.php?title=M100_Band3_Combine_6.4

## OBSNUM

A total of 46 (so far) science obsnum's were taken in the CO line (115.3 GHz). 7 of those are clearly
bad, and perhaps more.

We also have 36 pointing observations on RT-Vir, to check on the pointing.   These were observed in 7
nights in April/May 2022. April 5, 6, 7, 8, 27 and May 4, 17.

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
                                                                  

Current final RMS is down to just under 21 mK. Each dataset around 100mK. 100/sqrt(46-7)=16,
so not quite as good as expected.

Beam 1 always bad, Beam 5 often, Beam 6 has some low pattern, might be useful to try leaving it
out for all

## LMTOY Data Reduction

There are two ways to run the SLpipeline, using a different $WORK_LMT directory where the root
of the data processing occurs

1. Use the WORK_LMT that came with where **lmtoy** was installed. This will likely require
   write permission from the owner

   This is the way it runs on Unity.

2. Set WORK_LMT to a directory here in this directory,  something like

              WORK_LMT=`pwd`

   and no permissions in the $LMTOY tree are. Of course you still need to have LMTOY
   installed. The pipeline will then create all  data products in this local directory.

### Creating the run files

A master script **mk_runs** contains all the information on which obsnums are good,
which beams are good, etc.  You always will need to re-run this script to create the
SLpipeline *run* files. The script also uses the (optional) **OBSNUM.args** files, where
arguments specific to this obsnum can be stored. These files should be edited by
a user to create a new "final" dataset. Any optional post-processing after the
pipeline will not be described here (but is of course recommended?).

This command creates the run files (it uses the **mk_runs** scripts):

      make runs
	  
in this case just **2021-S1-US-3.run1** and **2021-S1-US-3.run2**

### Running the pipeline


With [SLURM](https://slurm.schedmd.com/documentation.html) this is the way:

      sbatch_lmtoy 2021-S1-US-3.run1
      # wait for it to finish
      sbatch_lmtoy 2021-S1-US-3.run2

whereas with [Gnu Parallel](https://www.gnu.org/software/parallel/)

      parallel --jobs 16 2021-S1-US-3.run1
      parallel --jobs 16 2021-S1-US-3.run2

can be submitted in a shell as the seond one will wait until the first one has finished
all pipeline calls. On "lma" this takes about 30 minutes to process all single obsnums
(run1) and a few combination maps (run2)

If you have no good parallel/batch processing available, the slow and trusted way is
via your [unix shell](https://www.gnu.org/software/bash/):

      bash 2021-S1-US-3.run1
      bash 2021-S1-US-3.run2

but this will take a while of course.

## Science:

### M100




## Files:


Description of the file that should be in this directory


      lmtinfo.txt               logfile from lmtinfo.py on all relevant science observations
      mk_runs.py                script to make the run files
      2021-S1-US-3.run1a        created by mk_runs
      2021-S1-US-3.run1b        created by mk_runs
      2021-S1-US-3.run2a        created by mk_runs
      2021-S1-US-3.run2b        created by mk_runs
      2021-S1-US-3/             (optional) directory with pipeline results, otherwise in $WORK_LMT

1. P R D R D P R D R D P                 01:15:04 04:27:29   8/8
2. P R D R D P				 05:07:45 06:32:44   0/4 - all bad (low elevation)
3. P R D R D P P P R D R D P P		 01:32:19 04:44:55   5/8 - 3 bad
4. R D P R D P P R D P R D P P		 01:18:20 04:20:57   8/8
5. P R D P R D P R D P R D P R D P	 22:45:35 03:22:22   10/10
6. P P P P P P P P R D P       	 	 23:10:45 03:46:56   2/2
7. P R D P D C P P R D P		 23:04:34 01:41:04   6/6

P   =  1.5 min
R,D = 12.0 min
