#! /usr/bin/env python
#
#   script generator for project="2021-S1-US-3"
#
#   lmtinfo.py grep US-3 Science Map | awk '{print $2}' | sort


import os
import sys

# in prep of the new lmtoy module
try:
    lmtoy = os.environ['LMTOY']
    sys.path.append(lmtoy + '/lmtoy')
    import runs
except:
    print("No LMTOY with runs.py")
    sys.exit(0)

project="2021-S1-US-3"

#        obsnums per source (make it negative if not added to the final combination)
on = {}
on['M100'] = [ 97520, 97521, 97523, 97524, 97528, 97529, 97531, 97532,
              -97740,-97741,-97743,-97744,                                             # apr 6
               97861, 97862, 97863, 97864, 97868, 97870, 97871,-97872,-97873,          # apr 8
               97993, 97994, 97999, 98000, 98004, 98006, 98007, 98011,-98012,
               98686, 98687, 98691, 98692, 98726, 98727, 98731, 98732, 98736, 98737,   # apr 27
               98974, 98975, 99674, 99675, 99679, 99680, 99702, 99703,                 # May 17
               ]

#        common parameters per source on the first dryrun (run1a, run2a)
pars1 = {}
pars1['M100'] = "dv=250 dw=300 extent=240"
pars1['M100'] = "dv=250 dw=300 extent=240 edge=1"

#        common parameters per source on subsequent runs (run1b, run2b)
pars2 = {}
pars2['M100'] = "pix_list=1,2,3,4,6,7,8,9,10,11,12,13,14,15"    # -0,-5


if True:
    print("new style")    
    runs.mk_runs(project, on, pars1, pars2)
    sys.exit(0)
else:
    print("old style")




