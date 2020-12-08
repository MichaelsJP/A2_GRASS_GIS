# !/usr/bin/env python3

from grass.pygrass.modules import Module
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import vector as v
import grass.script as gs

# Global vars
motorways = 'motorways@PERMANENT'
pop_layer = 'GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT'
motorways_buffered = 'motorways_buffered'
motorways_buffered_raster = 'motorways_buffered_raster'
# Global functions
v_to_rast = Module('v.to.rast')
r_stats_zonal = Module('r.stats.zonal')


def pop_calc(distance: int):
    motorways_buffered_population = 'motorways_buffered_population_' + str(distance)
    v.buffer(input=motorways, output=motorways_buffered, overwrite=True, distance=distance, type='line')
    v_to_rast(overwrite=True, input=motorways_buffered, output=motorways_buffered_raster, type='area', use='val',
              value=1)
    r_stats_zonal(base=motorways_buffered_raster, cover=pop_layer, method='sum', output=motorways_buffered_population,
                  overwrite=True, verbose=True)


def main():
    distances = [250, 500, 1000, 2500, 5000]
    for distance in distances:
        pop_calc(distance)


if __name__ == '__main__':
    main()
