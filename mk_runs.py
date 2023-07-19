#! /usr/bin/env python
#
#   script generator for project="2021-S1-US-3"
#
#   lmtinfo.py grep US-3 Science Map | awk '{print $2}' | sort


import os
import sys
from lmtoy import runs

project="2021-S1-US-3"

#        obsnums per source (make it negative if not added to the final combination)
on = {}
on['M100'] = [ 97520, 97521, 97523, 97524, 97528, 97529, 97531, 97532,                 # apr 5, 2022
              -97740,-97741,-97743,-97744,                                             # apr 6
               97861,-97862, 97863, 97864, 97870, 97871,-97872,-97873,                 # apr 8
               97993, 97994, 97999, 98000, 98006, 98007, 98011, 98012,
               98686, 98687, 98691, 98692, 98726, 98727, 98731, 98732, 98736, 98737,   # apr 27
               98974, 98975, 99674, 99675, 99679, 99680, 99702, 99703,                 # May 17
               ]

# pointing
on['RT-Vir'] = [97513, 97518, 97526, 97534, 97738, 97746, 97859, 97866, 97867, # 97868 (mislabaled)
                97875, 97879, 97996, 98002, 98009, 98014, 98016, 98684, 98689,
                98724, 98729, 98734, 98739, 98869, 98878, 98888, 98949, 98958,
                98968, 98970, 98972, 98977, 99672, 99677, 99682, 99683, 99705,
                ]

on['junk'] = []


#        common parameters per source on the first dryrun (run1a, run2a)
pars1 = {}
pars1['M100']   = "dv=250 dw=300 extent=220"
pars1['RT-Vir'] = "dv=250 dw=300 extent=120"
pars1['junk']   = ""

#        common parameters per source on subsequent runs (run1b, run2b)
pars2 = {}
pars2['M100']   = "pix_list=1,2,3,4,6,7,8,9,10,11,12,13,14,15"    # -0,-5
pars2['RT-Vir'] = ""
pars2['junk']   = ""

runs.mk_runs(project, on, pars1, pars2, sys.argv)
