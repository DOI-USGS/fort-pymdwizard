Spatial Content
********

Many data have an inherent spatial context that needs to be captured in
the metadata. At a minimum, one should record the geographic location where
the data were collected, generally called the extent or bounding box.

If the data are in a spatial data format, for example a shapefile or
raster, you will also need to document the spatial reference or
projection and how the data are organized spatially.

Setting the bounding coordinates manually.
------------------------------------------

If your data are in a non-spatial format, a .csv for example, you can
manually specify the bounding box interactively in the Spatial Tab. By
default new records in the Metadata Wizard 2.0 start with an extent set to
the whole world. This can be changed by editing the East, West, North, and
South coordinates in the text boxes to the left of the map. The map will
update to show the extent as specified in the text boxes.

If you do not know your bounding coordinates or would like to
interactively edit them, you can do so in the map to the right of the
text boxes. Click and drag one of the corner markers to resize the box.
The mouse wheel or +/- buttons in the upper left of the map can be used
to zoom the map. Clicking and dragging anywhere other than the corner
markers can be used to recenter the map. As you zoom the map in and
refine your extent additional detail will be displayed on the map to
help locate your study area. The layer button in the upper right can be
used to switch to a satellite imagery background.

When using the Biological Data Profile extension don’t forget to update the
Description of Geographic Extent element to match the bounding coordinates
displayed, e.g. Southwest United States, Colorado, Key West Florida, etc.

|

.. figure:: ../img/SpatialExtent.png
	:alt: Spatial Extent Editor
	
	Interface for editing the spatial extent
	
|

Auto-populating spatial content from data
-----------------------------------------

If your data are in a spatial data format the information for this
section can be auto-populated by pointing to the appropriate file. The
currently supported file types are: .shp, .tif, .jpg, .bmp, .img, .png,
.grd. In addition to extracting the data’s extent the coordinate
system/projection and spatial data organization will be extracted. For
this functionality to work the data must have a defined projection. Note
that some less common projections might display incorrectly, so do check
that the values imported are appropriate.
