# just to show how it's done....
# some of these steps take a long time

help:
	@echo no help yet

all:
	casa -c M100_casaguide64.py
	./convert1.py
	./mk_fluxes.sh
	./cumflux.py

#   LMTOY is needed, plus all the 2021-S1-US-3 data
lmt:
	../mk_runs.py
	bash ../2021-S1-US-3.run1a
	bash ../2021-S1-US-3.run1b
	bash ../2021-S1-US-3.run2a
	bash ../2021-S1-US-3.run2b
