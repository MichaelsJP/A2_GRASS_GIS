###2.1   
v.import input=/home/jules/workspace/University/fossgis_WS_2020/A2_GRASS_GIS/data layer=motorways output=motorways --overwrite   
###2.2   
v.import input=/home/jules/workspace/University/fossgis_WS_2020/A2_GRASS_GIS/data layer=gadm28_adm2_germany output=gadm28_adm2_germany --overwrite   
###2.3   
r.import input=/home/jules/workspace/University/fossgis_WS_2020/A2_GRASS_GIS/data/GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3/GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3.tif output=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3 --overwrite   
###3.1   
g.region -s vector=gadm28_adm2_germany@PERMANENT res=250                                         
###3.2   
v.to.rast --overwrite input=gadm28_adm2_germany@PERMANENT type=boundary,area output=gadm28_adm2_germany_raster@PERMANENT use=attr attribute_column=OBJECTID

###3.3
r.stats.zonal --overwrite base=gadm28_adm2_germany_raster@PERMANENT cover=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT method=sum output=POP_DISTRICT_RESULT

###3.4
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

###4
#### Set region
g.region vector=motorways@PERMANENT res=250                           
v.buffer --overwrite input=motorways@PERMANENT type=line output=motorways_buffered@PERMANENT distance=1000   
v.to.rast --overwrite input=motorways_buffered@PERMANENT output=motorways_buffered_raster use=val   
r.stats.zonal --overwrite base=motorways_buffered_raster@PERMANENT cover=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT method=sum output=motorways_buffered_population   

The number of people living in 1km of the roads is around 486.948.

