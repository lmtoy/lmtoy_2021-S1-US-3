# 2021-S1-US-3

This project observed M100 in the CO(1-0) 115 GHz transition. One of the science goals is to learn
more about how important data combination of interferometric and single dish is. A background
example of this is discussed in https://casaguides.nrao.edu/index.php?title=M100_Band3_Combine_6.4

## OBSNUM

A total of 46 (so far) science obsnum's were taken in the CO line (115.3 GHz). 7 of those are clearly
bad, and perhaps more.

Current RMS is down to 21 mK, but the current last combination up to 99703 has bad data included,
as the mom0 looks bad. The combo  up through 98737 looks in fact much better (rms 24 mK)

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


      lmtinfo.log               logfile from lmtinfo.py on all relevant science observations
      mk_runs                   script to make the run files
      2021-S1-US-3.run1         created by mk_runs
      2021-S1-US-3.run2         created by mk_runs
      2021-S1-US-3/             (optional) directory with pipeline results, otherwise in $WORK_LMT
