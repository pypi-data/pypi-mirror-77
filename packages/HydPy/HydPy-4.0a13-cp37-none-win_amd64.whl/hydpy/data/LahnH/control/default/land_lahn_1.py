# -*- coding: utf-8 -*-

from hydpy.models.hland_v1 import *

simulationstep("1h")
parameterstep("1d")

area(1660.2)
nmbzones(13)
zonetype(FIELD, FOREST, FIELD, FOREST, FIELD, FOREST, FIELD, FOREST, FIELD,
         FOREST, FIELD, FOREST, FOREST)
zonearea(25.61, 1.9, 467.41, 183.0, 297.12, 280.53, 81.8, 169.66, 36.0,
         100.83, 2.94, 11.92, 1.48)
zonez(2.0, 2.0, 3.0, 3.0, 4.0, 4.0, 5.0, 5.0, 6.0, 6.0, 7.0, 7.0, 8.0)
zrelp(3.45)
zrelt(3.45)
zrele(2.513)
pcorr(auxfile='land')
pcalt(0.1)
rfcf(0.885)
sfcf(1.3203)
tcalt(0.6)
ecorr(1.0)
ecalt(0.0)
epf(0.02)
etf(0.1)
ered(0.0)
ttice(nan)
icmax(auxfile='land')
tt(0.59365)
ttint(2.0)
dttm(0.0)
cfmax(field=5.0, forest=3.0)
gmelt(0.0)
cfr(0.05)
whc(0.1)
fc(206.0)
lp(0.9)
beta(1.45001)
percmax(1.02978)
cflux(0.0)
resparea(auxfile='land')
recstep(1200.0)
alpha(auxfile='land')
k(0.0053246701322556935)
k4(0.0413)
gamma(0.0)
maxbaz(0.80521)
abstr(0.0)
