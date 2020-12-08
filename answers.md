**Exercise** 2 - 08.12.2020\
**Course**:  Fossgis 2020/21\
**Instructor**: Christina Ludwig\
**Assignee**: Julia Campbell, Julian Psotta
---

### 2.1

v.import input=/home/jules/workspace/University/fossgis_WS_2020/A2_GRASS_GIS/data layer=motorways output=motorways
--overwrite

### 2.2

v.import input=/home/jules/workspace/University/fossgis_WS_2020/A2_GRASS_GIS/data layer=gadm28_adm2_germany
output=gadm28_adm2_germany --overwrite

### 2.3

r.import
input=/home/jules/workspace/University/fossgis_WS_2020/A2_GRASS_GIS/data/GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3/GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3.tif
output=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3 --overwrite

### 3.1

g.region -s vector=gadm28_adm2_germany@PERMANENT res=250

### 3.2

v.to.rast --overwrite input=gadm28_adm2_germany@PERMANENT type=boundary,area output=gadm28_adm2_germany_raster@PERMANENT
use=attr attribute_column=OBJECTID

### 3.3

r.stats.zonal --overwrite base=gadm28_adm2_germany_raster@PERMANENT
cover=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT method=sum output=POP_DISTRICT_RESULT

### 3.4

```
Ortenaukreis:  415.512
Offiziell: 429.479
```

```
Rottweil: 135.473
Offiziell: 139.455
```

```
Baden-Baden: 52.055
Offiziell: 55.123
```

The data is comparably good to the official numbers from the Statistisches Bundesamt.

### 4

#### Set region

g.region vector=motorways@PERMANENT res=250                           
v.buffer --overwrite input=motorways@PERMANENT type=line output=motorways_buffered@PERMANENT distance=1000   
v.to.rast --overwrite input=motorways_buffered@PERMANENT output=motorways_buffered_raster use=val   
r.stats.zonal --overwrite base=motorways_buffered_raster@PERMANENT
cover=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT method=sum output=motorways_buffered_population

The number of people living in 1km of the roads is around 486.948.

### 5

```python
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

```