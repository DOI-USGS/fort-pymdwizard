===============
Spatial Content
===============

Many data have an inherent spatial context that needs to be captured in
the metadata. At a minimum, one should record the geographic location where
the data were collected, generally called the extent or bounding box.

If the data are in a spatial data format, for example a shapefile or
raster, the user will also need to document the spatial reference or map
projection and how the data are organized spatially.

Manually Setting the Bounding Coordinates
-----------------------------------------

If the data are in a non-spatial format, for example a Comma Separated Values (CSV) file, 
the bounding box can be manually specified interactively in the Spatial tab. By
default, new records in the Metadata Wizard start with a global geographic extent.
This can be changed by editing the East, West, North, and
South coordinates in the text boxes to the left of the map. The map will
update to show the extent as specified in the text boxes.

Alternatively, the user can use the map to define or edit the bounding coordinates. 
Click and drag one of the corner markers to resize the box.
The mouse wheel or +/- buttons in the upper left of the map can be used
to zoom the map. Clicking and dragging anywhere other than the corner
markers can be used to center the map. As the map is zoomed in, refining the extent,
additional detail will be displayed to help locate the study area. The layer 
button in the upper right can be used to toggle between satellite imagery and the OpenStreetMap background.

When using the Biological Data Profile extension do not forget to update the
Description of Geographic Extent element to match the bounding coordinates
displayed, for example, Southwest United States, Colorado, Key West, Florida.

|

.. figure:: ../img/SpatialExtent.png
	:alt: Spatial Extent Editor
	
	Interface for editing the spatial extent
	
|

Auto-Populating Spatial Content From Data
-----------------------------------------

If the data are in a spatial data format, the information for this
section can be auto-populated by pointing to the appropriate file. 

File types that are currently supported for auto-populating spatial content are: 

-  Shapefile (.shp) 
-  GeoTIFF (.tif) 
-  JPEG (.jpg) 
-  Bitmap (.bmp) 
-  Disk Image File (.img) 
-  Portable Network Graphics (.png)
-  ASCII Grid (.grd) 

In addition to extracting the data’s extent, the coordinate
system/map projection and spatial data organization will be extracted. For
this functionality to work, the data must have a defined coordinate system 
(a reference system used to represent the locations of geographic features). Note
that some less common projections might display incorrectly, so do check
that the values imported are appropriate.
