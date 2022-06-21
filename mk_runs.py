#! /usr/bin/env python
#
#   script generator for project="2021-S1-US-3"
#
#   lmtinfo.py grep US-3 Science Map | awk '{print $2}' | sort


import os
import sys

project="2021-S1-US-3"

#        obsnums per source (make it negative if not added to the final combination)
on = {}
on['M100'] = [ 97520, 97521, 97523, 97524, 97528, 97529, 97531, 97532,
              -97740,-97741,-97743,-97744,
               97861, 97862, 97863, 97864, 97868, 97870, 97871,-97872,-97873,
               97993, 97994, 97999, 98000, 98004, 98006, 98007, 98011,-98012,
               98686, 98687, 98691, 98692, 98726, 98727, 98731, 98732, 98736, 98737,
               98974, 98975, 99674, 99675, 99679, 99680, 99702, 99703,                 # May 17
               ]

#        common parameters per source on the first dryrun (run1, run2)
pars1 = {}
pars1['M100'] = "dv=250 dw=300 extent=240 edge=1"

#        common parameters per source on subsequent runs (run1a, run2a)
pars2 = {}
pars2['M100'] = "pix_list=1,2,3,4,6,7,8,9,10,11,12,13,14,15"


# below here no need to change code
# ========================================================================

#        helper function for populating obsnum dependant argument
def getargs(obsnum):
    """ search for <obsnum>.args
    """
    f = "%d.args" % obsnum
    if os.path.exists(f):
        lines = open(f).readlines()
        args = ""
        for line in lines:
            if line[0] == '#': continue
            args = args + line.strip() + " "
        return args
    else:
        return ""

#        specific parameters per obsnum will be in files <obsnum>.args
pars3 = {}
for s in on.keys():
    for o1 in on[s]:
        o = abs(o1)
        pars3[o] = getargs(o)


run1  = '%s.run1'  % project
run1a = '%s.run1a' % project
run2  = '%s.run2' % project
run2a = '%s.run2a' % project

fp1 = open(run1,  "w")
fp2 = open(run1a, "w")
fp3 = open(run2,  "w")
fp4 = open(run2a, "w")

#                           single obsnum
n1 = 0
for s in on.keys():
    for o1 in on[s]:
        o = abs(o1)
        cmd1 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 restart=1 " % (o,s,pars1[s])
        cmd2 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 %s" % (o,s,pars2[s], pars3[o])
        fp1.write("%s\n" % cmd1)
        fp2.write("%s\n" % cmd2)
        n1 = n1 + 1

#                           combination obsnums
n2 = 0        
for s in on.keys():
    obsnums = ""
    n3 = 0
    for o1 in on[s]:
        o = abs(o1)
        if o1 < 0: continue
        n3 = n3 + 1
        if obsnums == "":
            obsnums = "%d" % o
        else:
            obsnums = obsnums + ",%d" % o
    print('%s[%d/%d] :' % (s,n3,len(on[s])), obsnums)
    cmd3 = "SLpipeline.sh _s=%s admit=0 restart=1 obsnums=%s" % (s, obsnums)
    cmd4 = "SLpipeline.sh _s=%s admit=1 srdp=1  obsnums=%s" % (s, obsnums)
    fp3.write("%s\n" % cmd3)
    fp4.write("%s\n" % cmd4)
    n2 = n2 + 1

print("A proper re-run of %s should be in the following order:" % project)
print(run1)
print(run2)
print(run1a)
print(run2a)
print("Where there are %d single obsnum runs, and %d combination obsnums" % (n1,n2))