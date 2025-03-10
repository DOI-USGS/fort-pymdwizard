#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module provide a variety of spatial introspection functions.
Produces FGDC spatial elements from spatial data sets


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey 
(USGS). Although the software has been subjected to rigorous review,
the USGS reserves the right to update the software as needed pursuant to
further analysis and review. No warranty, expressed or implied, is made by
the USGS or the U.S. Government as to the functionality of the software and
related material nor shall the fact of release constitute any such warranty.
Furthermore, the software is released on condition that neither the USGS nor
the U.S. Government shall be held liable for any damages resulting from
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""

import os
import collections
import math

import numpy as np
import pandas as pd

from pymdwizard.core.xml_utils import xml_node
from pymdwizard.core import utils
from pymdwizard.core import data_io

try:
    from osgeo import gdal
    from osgeo import osr
    from osgeo import ogr

    gdal.UseExceptions()
    gdal.AllRegister()
    use_gdal = True
except ImportError:
    print("ERROR Importing GDAL, Spatial functionality limited")
    use_gdal = False

try:
    import laspy
    use_laspy = True
except ImportError:
    print("ERROR Importing laspy, LAS functionality limited")
    use_laspy = False

def set_local_gdal_data():
    """
    Sets the path variable to the local gdal instance

    Returns
    -------
    None
    """
    python_root = utils.get_install_dname("python")
    gdal_data = os.path.join(python_root, "Library", "share", "gdal")
    os.environ["GDAL_DATA"] = gdal_data


def _get_las_extent(fh):
    """
    Extract the projected extent from a LAS file header.
    (min_x, max_x, min_y, max_y)

    Parameters
    ----------
    fh : LAS file handle
        A file handle that provides access to the LAS file header.

    Returns
    -------
    (min_x, max_x, min_y, max_y) : tuple
        A tuple containing the upper left x-coordinate (min_x), 
        lower right x-coordinate (max_x), lower right y-coordinate (min_y), 
        and upper left y-coordinate (max_y) of the LAS file extent.
    """
    header = fh.header
    ulx = header.x_min
    lrx = header.x_max
    uly = header.y_max
    lry = header.y_min
    return ulx, lrx, lry, uly

def _get_raster_extent(src):
    """
    extract projected extent from a raster dataset
    (min_x, max_x, min_y, max_y)

    Parameters
    ----------
    src : gdal raster

    Returns
    -------
    (min_x, max_x, min_y, max_y)
    """
    ulx, xres, xskew, uly, yskew, yres = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    return ulx, lrx, lry, uly


def get_extent(layer):
    """
    returns projected extent from an ogr layer or gdal dataset
    (min_x, max_x, min_y, max_y)

    Parameters
    ----------
    layer : ogr layer or gdal dataset

    Returns
    -------
    (min_x, max_x, min_y, max_y)
    """
    try:
        return layer.GetExtent()
    except:
        pass

    try:
        return _get_las_extent(layer)
    except:
        pass

    try:
        return _get_raster_extent(layer)
    except:
        pass

def get_geographic_extent(layer):
    """
    returns extent in geographic (lat, long) coordinates

    Parameters
    ----------
    layer : ogr layer or gdal dataset

    Returns
    -------
    (min_x, max_x, min_y, max_y)
    """
    
    min_x, max_x, min_y, max_y = get_extent(layer)
    srs = get_ref(layer)
    srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    # Get the body (planet or moon) from the projection definition
    # removes the lock-in to EPSG:4326 (WGS84)
    target = srs.CloneGeogCS()
    target.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

    try:
        spatialRef = layer.GetSpatialRef()
        spatialRef.ExportToProj4()
        spatialRef.AutoIdentifyEPSG()
        spref = spatialRef.GetAuthorityCode(None)
    except:
        pass
    
    west, east, south, north = calculate_max_bounds(min_x, max_x, min_y, max_y, srs, target)

    return west, east, south, north


def calculate_max_bounds(min_x, max_x, min_y, max_y, src_srs, target_srs):
    """
    Calculates the maximum east, minimum west, maximum north, and minimum south
    coordinates after transforming the points from the source SRS to the target SRS.

    Parameters:
    - min_x, max_x: The extent of the x-coordinates.
    - min_y, max_y: The extent of the y-coordinates.
    - src_srs: The source spatial reference system.
    - target_srs: The target spatial reference system.

    Returns:
    - (max_east, min_west, max_north, min_south): Tuple of calculated bounds.
    """
    steps = 10

    # Initialize the values for each direction
    max_east = -float('inf')
    min_west = float('inf')
    max_north = -float('inf')
    min_south = float('inf')

    # Calculate max_east and min_west
    for step in range(steps + 1):
        cur_north = min_y + step * ((max_y - min_y) / steps)

        # Max East
        transformed_east = transform_point((max_x, cur_north), src_srs, target_srs)
        if transformed_east[0] > max_east:
            max_east = transformed_east[0]

        # Min West
        transformed_west = transform_point((min_x, cur_north), src_srs, target_srs)
        if transformed_west[0] < min_west:
            min_west = transformed_west[0]

    # Calculate max_north and min_south
    for step in range(steps + 1):
        cur_east = min_x + step * ((max_x - min_x) / steps)

        # Max North
        transformed_north = transform_point((cur_east, max_y), src_srs, target_srs)
        if transformed_north[1] > max_north:
            max_north = transformed_north[1]

        # Min South
        transformed_south = transform_point((cur_east, min_y), src_srs, target_srs)
        if transformed_south[1] < min_south:
            min_south = transformed_south[1]

    return min_west, max_east, max_north, min_south

def get_ref(layer):
    """
    returns the  osr geospatial reference from an object

    Parameters
    ----------
    layer : ogr layer or gdal dataset

    Returns
    -------
    osr  geospatial reference
    """
    try:
        wkt = layer.GetProjection()
    except:
        pass

    try:
        wkt = layer.header.parse_crs().to_wkt()
    except:
        pass

    try:
        wkt = layer.GetSpatialRef().ExportToWkt()
    except:
        pass

    return osr.SpatialReference(wkt=wkt)


def get_latlong_res(extent):
    # D. Ignizio : This function is a modified approach to calculating
    # latitudinal and longitudinal resolution in a GCS.
    # Use in lieu of Vincenty's algorithm due to complexity/issues with
    # incorrect results.
    # The formula calculates values against the WGS 84 spheroid.
    # The mid-point of the latitudinal extent of the dataset is used to
    # calculate values, as they change depending on where on the globe
    # we are considering.

    ### Find GCS bounding coordinates of DS
    min_lon, max_lon, min_lat, max_lat = extent

    ### Find mid-latitude position while handling Hemisphere
    mid = 0
    if max_lat >= min_lat:
        mid = ((max_lat - min_lat) / 2) + min_lat
    if max_lat < min_lat:
        mid = ((min_lat - max_lat) / 2) + max_lat
    mid_lat = mid

    ##########################################################
    # For a WGS 84 Spheroid. See: http://en.wikipedia.org/wiki/Latitude
    # Also see: pg. 71 of the Biological Data Profile Workbook (FGDC, 2001)
    # The following points were plotted and a third-order polynomial
    # equation was generated in MS Excel.

    # @ Degree    1 Degree Latitude (= to km)    1 Degree Longitude (= to km)
    #       0         110.574                       111.32
    #       15        110.649                       107.55
    #       30        110.852                       96.486
    #       45        111.132                       78.847
    #       60        111.412                       55.8
    #       75        111.618                       28.902
    #       90        111.694                       0
    ##########################################################

    # Length of 1 degree of Latitude in kilometers @ Latitude(y) on the globe.
    # y = -3E-06x^3 + 0.0005x^2 - 0.0013x + 110.57
    x = mid_lat
    len1_degree_lat = (
        (-3e-06 * pow(x, 3)) + (0.0005 * pow(x, 2)) - (0.0013 * x) + 110.57
    )
    len1_minute_lat = len1_degree_lat / 60
    len1_second_lat = len1_minute_lat / 60

    data_scale = 24000
    dig_precision = 0.001

    latlat_reses = float(
        (1 / len1_second_lat)
        * (1 / 3280.84)
        * float(data_scale)
        * float(1.0 / 12.0)
        * float(dig_precision)
    )
    latlat_reses = str(format(latlat_reses, ".10f"))

    # Length of 1 degree of Longitude in kilometers @ Latitude(y) on the globe.
    # y = 7E-05x^3 - 0.0203x^2 + 0.0572x + 111.24

    len1_degree_long = (
        (7e-05 * pow(x, 3)) - (0.0203 * pow(x, 2)) + (0.0572 * x) + 111.24
    )
    len1_minute_long = len1_degree_long / 60
    len1_second_long = len1_minute_long / 60

    long_res = float(
        (1 / len1_second_long)
        * (1 / 3280.84)
        * float(data_scale)
        * float(1.0 / 12)
        * float(dig_precision)
    )
    long_res = str(format(long_res, ".10f"))

    return latlat_reses, long_res


def get_abs_resolution(src, params):

    # The minimum difference between X (abscissa) and Y (ordinate) values in
    #  the planar data set
    # The values usually indicate the ?fuzzy tolerance? or ?clustering? setting
    #   that establishes the minimum distance at which two points will NOT be
    #   automatically converged by the data collection device (digitizer,
    #   GPS, etc.). NOTE: units of measures are provided under element Planar
    #   Distance Units
    # Raster data: Abscissa/ordinate res equals cell resolution
    # Vector data: Abscissa/ordinate res is the smallest measurable distance
    try:
        # this will only work for raster data
        xform = src.GetGeoTransform()
        params["absres"] = math.fabs(xform[1])
        params["latres"] = math.fabs(xform[1])
        params["ordres"] = math.fabs(xform[5])
        params["longres"] = math.fabs(xform[5])

    except:
        # otherwise we will calculate these from our projection parameters
        if params["mapprojn"] != "Unknown":
            data_scale = 24000
            dig_precision = 0.001

            # Industry-standard digitizer precision of 0.001"
            if params["plandu"].lower() == "feet":
                params["absres"] = str(float(data_scale) * float(dig_precision) / 12.0)
                params["ordres"] = str(float(data_scale) * float(dig_precision) / 12.0)
            elif params["plandu"].lower() == "meter":
                params["absres"] = str(
                    float(data_scale) * (float(dig_precision) / 12.0) * 0.3048
                )
                params["ordres"] = str(
                    float(data_scale) * (float(dig_precision) / 12.0) * 0.3048
                )
            else:
                # default to meters?
                params["absres"] = str(
                    float(data_scale) * (float(dig_precision) / 12.0) * 0.3048
                )
                params["ordres"] = str(
                    float(data_scale) * (float(dig_precision) / 12.0) * 0.3048
                )
        else:
            params["absres"] = params["latres"]
            params["ordres"] = params["longres"]


def get_params(layer):

    # get the spatial reference and extent
    ref = get_ref(layer)
    projected_extent = get_extent(layer)
    geographic_extent = get_geographic_extent(layer)

    params = {}

    params["latres"], params["longres"] = get_latlong_res(geographic_extent)
    params["latres"], params["longres"] = str(params["latres"]), str(params["longres"])
    params["geogunit"] = "Decimal seconds"  # we will always use Decimal Seconds'
    params["mapprojn"] = ref.GetAttrValue("projcs")
    params["projection_name"] = ref.GetAttrValue("projection")
    params["geogcs"] = ref.GetAttrValue("geogcs")
    params["stdparll"] = str(ref.GetProjParm(osr.SRS_PP_STANDARD_PARALLEL_1))
    params["stdparll_2"] = str(ref.GetProjParm(osr.SRS_PP_STANDARD_PARALLEL_2))
    params["longcm"] = str(ref.GetProjParm(osr.SRS_PP_CENTRAL_MERIDIAN))
    params["latprjo"] = str(ref.GetProjParm(osr.SRS_PP_LATITUDE_OF_ORIGIN))
    params["feast"] = str(ref.GetProjParm(osr.SRS_PP_FALSE_EASTING))
    params["fnorth"] = str(ref.GetProjParm(osr.SRS_PP_FALSE_NORTHING))
    params["sfequat"] = str(ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR))
    params["heightpt"] = str(ref.GetProjParm(osr.SRS_PP_PERSPECTIVE_POINT_HEIGHT))
    params["longpc"] = str(ref.GetProjParm(osr.SRS_PP_LONGITUDE_OF_CENTER))
    params["latprjc"] = str(ref.GetProjParm(osr.SRS_PP_LATITUDE_OF_CENTER))
    params["latprjo"] = str(ref.GetProjParm(osr.SRS_PP_LATITUDE_OF_CENTER))
    params["sfctrlin"] = str(ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR))
    params["obqlazim"] = "Unknown"
    params["azimangl"] = str(ref.GetProjParm(osr.SRS_PP_AZIMUTH))
    params["azimptl"] = str(ref.GetProjParm(osr.SRS_PP_LONGITUDE_OF_ORIGIN))
    params["obqlpt"] = "Unknown"
    params["obqllat"] = "Unknown"
    params["obqllong"] = "Unknown"
    params["svlong"] = str(ref.GetProjParm(osr.SRS_PP_LATITUDE_OF_ORIGIN))
    params["sfprjorg"] = "Unknown"
    params["landsat"] = str(ref.GetProjParm(osr.SRS_PP_LANDSAT_NUMBER))
    params["pathnum"] = str(ref.GetProjParm(osr.SRS_PP_PATH_NUMBER))
    params["sfctrmer"] = str(ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR))
    params["gridsysn"] = "Unknown"
    params["utmzone"] = ref.GetUTMZone()
    if params["utmzone"] == 0:
        params["utmzone"] = "Unknown"
    params["upszone"] = "Unknown"
    params["spcszone"] = "Unknown"
    params["arczone"] = "Unknown"
    params["othergrd"] = "Unknown"
    params["localpd"] = "Unknown"
    params["localpgi"] = "Unknown"
    if isinstance(layer, gdal.Dataset):
        params["plance"] = "row and column"
    else:
        params["plance"] = "coordinate pair"
    params["distres"] = "Unknown"
    params["bearres"] = "Unknown"
    params["bearunit"] = "Unknown"
    params["bearrefd"] = "Unknown"
    params["bearrefm"] = "Unknown"
    params["plandu"] = ref.GetLinearUnitsName()
    params["localdes"] = "Unknown"
    params["localgeo"] = "Unknown"
    params["horizdn"] = ref.GetAttrValue("datum")
    params["ellips"] = ref.GetAttrValue("spheroid")
    params["localpd"] = "Unknown"
    params["semiaxis"] = str(ref.GetSemiMajor())
    params["denflat"] = str(ref.GetInvFlattening())
    params["altdatum"] = ref.GetAttrValue("VertCSName")
    params["altres"] = "Unknown"
    params["altunits"] = "Unknown"
    params["altenc"] = "Unknown"
    params["depthdn"] = "Unknown"
    params["depthres"] = "Unknown"
    params["depthdu"] = "Unknown"
    params["depthem"] = "Unknown"

    for k in params:
        if params[k] is None:
            params[k] = "Unknown"

    get_abs_resolution(layer, params)

    # SPCS_Zone
    if params["mapprojn"] != None and "stateplane" in params["mapprojn"].lower():
        parts = params["mapprojn"].split("_")
        params["spcszone"] = str(parts[parts.index("FIPS") + 1])
    else:
        params["spcszone"] = "Unknown"

    # ARC_Zone
    if params["mapprojn"] != None and "_arc_system" in params["mapprojn"].lower():
        parts = params["mapprojn"].split("_")
        params["arczone"] = str(parts[-1])
    else:
        params["arczone"] = "Unknown"

    # PCS_Units
    params["upzone"] = "Unknown"

    return params


def transform_point(xy, from_srs, to_srs):
    """
    Transforms a point from one srs to another

    Parameters
    ----------
    x : float
    y : float
    from_srs : ogr projection
    to_srs : ogr projection

    Returns
    -------
    (x, y) : (float, float)
    """
    coord_xform = osr.CoordinateTransformation(from_srs, to_srs)
    y_round = round(xy[1], 8)
    x_round = round(xy[0], 8)

    results = coord_xform.TransformPoint(x_round, y_round)
    return results[0], results[1]


def get_layer(fname, feature_class=None):
    """
    Type agnostic function for opening a file without specifying it's type


    Parameters
    ----------
    fname : str
            The filename and path to the file to open
    feature_class : str (optional)
            If the fname is a file geodatabase then
            the feature class name is required

    Returns
    -------
    Either a gdal Dataset or a ogr layer depending on the input
    """
    if fname.endswith(".shp"):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        global dataset
        dataset = driver.Open(fname)
        return dataset.GetLayer()
    elif fname.endswith(".gdb"):
        driver = ogr.GetDriverByName("OpenFileGDB")
        global gdb
        gdb = driver.Open(fname, 0)
        return gdb.GetLayerByName(feature_class)
    elif fname.endswith(".las") or fname.endswith(".laz"):
        fh = laspy.open(fname)
        return fh
    else:
        # it better be a raster
        return gdal.Open(fname)

    return None


def get_spref(fname, feature_class=None):
    """
    Returns the fgdc xml element with the spatial reference extracted from a
    dataset

    Parameters
    ----------
    fname : str
            The filename and path to the file to open
    feature_class : str (optional)
            If the fname is a file geodatabase then
            the feature class name is required

    Returns
    -------
    ogr spatial reference object
    """
    layer = get_layer(fname, feature_class=feature_class)

    params = get_params(layer)

    spref = xml_node("spref")
    horizsys = xml_node("horizsys", parent_node=spref)

    if params["mapprojn"] == "Unknown":
        geographic_node = geographic(params)
        horizsys.append(geographic_node)

    else:
        planar_node = planar(params)
        horizsys.append(planar_node)

    geodetic_node = geodetic(params)
    horizsys.append(geodetic_node)

    return spref


def geographic(params):
    """

    Parameters
    ----------
    params : dict
            (returned from:

    Returns
    -------
    fgdc <geograph> element
    """
    geograph = xml_node("geograph")
    latres = xml_node("latres", params["latres"], geograph)
    longres = xml_node("longres", params["longres"], geograph)
    geounit = xml_node("geogunit", params["geogunit"], geograph)
    return geograph


def mapproj(params):
    mapproj_node = xml_node("mapproj")

    fgdc_name, function = lookup_fdgc_projname(
        params["projection_name"], params["mapprojn"]
    )
    if fgdc_name is None:
        fgdc_name = params["projection_name"]
        prj_node = unknown_projection(params)
    else:
        prj_node = function(params)
    mapprojn = xml_node("mapprojn", text=fgdc_name, parent_node=mapproj_node)
    mapproj_node.append(prj_node)
    return mapproj_node


def planar(params):
    planar = xml_node("planar")
    if params["utmzone"] != "Unknown":
        top_node = utm(params)
    elif params["spcszone"] != "Unknown":
        top_node = spcs(params)
    elif params["arczone"] != "Unknown":
        top_node = arc(params)
    elif params["mapprojn"] != "Unknown":
        top_node = mapproj(params)

    planar.append(top_node)

    planci = xml_node("planci", parent_node=planar)
    plance = xml_node("plance", text=params["plance"], parent_node=planci)
    coordrep = xml_node("coordrep", parent_node=planci)
    absres = xml_node("absres", text=params["absres"], parent_node=coordrep)
    ordres = xml_node("ordres", text=params["ordres"], parent_node=coordrep)
    plandu = xml_node("plandu", text=params["plandu"], parent_node=planci)

    return planar


def geodetic(params):
    """

    Parameters
    ----------
    params : dict
            (returned from:

    Returns
    -------
    fgdc <geograph> element
    """
    geodetic = xml_node("geodetic")
    xml_node("horizdn", params["horizdn"], geodetic)
    xml_node("ellips", params["ellips"], geodetic)
    xml_node("semiaxis", params["semiaxis"], geodetic)
    xml_node("denflat", params["denflat"], geodetic)
    return geodetic


def albers_conic_equal_area(params):

    """
    returns lxml nodes that contain projection parameters for fgdc
    Albers Conic Equal Area projection

    stdparll = First standard parallel
    stdparl_2 = Second standard parallel (if exists)
    longcm = Longitude of Central Meridian
    latprjo = Latitude of Projection Origin
    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc Albers Conic Equal Area projection
    """

    albers = xml_node("albers")
    stdparll = xml_node("stdparll", params["stdparll"], albers)
    if params["stdparll_2"]:
        stdparll_2 = xml_node("stdparll", params["stdparll_2"], albers)

    for item in ["longcm", "latprjo", "feast", "fnorth"]:
        xml_node(item, params[item], albers)
    return albers


def azimuthal_equidistant(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Azimuthal Equidistant projection

    longcm = Longitude of Central Meridian
    latprjo = Latitude of Projection Origin
    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params
    Returns
    -------
    lxml nodes for fgdc Azimuthal Equidistant projection
    """

    # This section should probably be handled in a different function?
    # planar = xml_node('planar')
    # mapproj = xml_node('mapproj', parent_node=planar)
    # mapprojn = xml_node('mapprojn', params['mapprojn'], mapproj)

    azimequi = xml_node("azimequi")
    longcm = xml_node("longcm", params["longcm"], azimequi)
    latprjo = xml_node("latprjo", params["latprjo"], azimequi)
    feast = xml_node("feast", params["feast"], azimequi)
    fnorth = xml_node("fnorth", params["fnorth"], azimequi)
    return azimequi


def equidistant_conic(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Equidistant Conic projection

    stdparll = First standard parallel
    stdparl_2 = Second standard parallel (if exists)
    longcm = Longitude of Central Meridian
    latprjo = Latitude of Projection Origin
    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc Equidistant Conic projection
    """

    equicon = xml_node("equicon")
    stdparll = xml_node("stdparll", params["stdparll"], equicon)
    if params["stdparll_2"] != "Unknown":
        stdparll_2 = xml_node("stdparll", params["stdparll_2"], equicon)

    for item in ["longcm", "latprjo", "feast", "fnorth"]:
        xml_node(item, params[item], equicon)
    return equicon


def unknown_projection(params):
    mapprojp = xml_node("mapprojp")

    if params["stdparll"] != "Unknown":
        stdparll = xml_node("stdparll", params["stdparll"], mapprojp)
    if params["stdparll_2"] != "Unknown":
        stdparll_2 = xml_node("stdparll", params["stdparll_2"], mapprojp)

    for k in [
        "longcm",
        "latprjo",
        "feast",
        "fnorth",
        "sfequat",
        "heightpt",
        "longpc",
        "latprjc",
        "sfctrlin",
        "obqlazim",
        "azimangl",
        "azimptl",
    ]:
        print(k)
        if params[k] not in ["Unknown", "unknown"]:
            xml_node(k, params[k], mapprojp)
    return mapprojp


def equirectangular(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Equirectangular projection

    stdparll = First standard parallel
    longcm = Longitude of Central Meridian
    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc Equirectangular projection
    """
    equirect = xml_node("equirect")
    stdparll = xml_node("stdparll", params["stdparll"], equirect)
    longcm = xml_node("longcm", params["longcm"], equirect)
    feast = xml_node("feast", params["feast"], equirect)
    fnorth = xml_node("fnorth", params["fnorth"], equirect)
    return equirect


def general_vertical_near_sided_perspective(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    General Vertical Near-sided Perspective projection

    heightpc = Height of perspective point above surface
    longpc = Longitude of projection center
    latprjc = Latitude of projection center
    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc General Vertical Near-sided Perspective projection
    """
    gvnsp = xml_node("gvnsp")
    heightpt = xml_node("heightpt", params["heightpt"], gvnsp)
    longpc = xml_node("longpc", params["longpc"], gvnsp)
    latprjc = xml_node("latprjc", params["latprjc"], gvnsp)
    feast = xml_node("feast", params["feast"], gvnsp)
    fnorth = xml_node("fnorth", params["fnorth"], gvnsp)
    return gvnsp


def gnomonic(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Gnomonic projection

    longpc = Longitude of Projection Center
    latprjc = Latitude of Projection Center
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc Gnomonic projection
    """
    gnomonic = xml_node("gnomonic")
    longpc = xml_node("longpc", params["longpc"], gnomonic)
    latprjc = xml_node("latprjc", params["latprjc"], gnomonic)
    feast = xml_node("feast", params["feast"], gnomonic)
    fnorth = xml_node("fnorth", params["fnorth"], gnomonic)
    return gnomonic


def lambert_azimuthal_equal_area(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Lambert Azimuthal Equal Area projection

    longpc = Longitude of Projection Center
    latprjc = Latitude of Projection Center
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Lambert Azimuthal Equal Area projection
    """
    lamberta = xml_node("lamberta")
    longpc = xml_node("longpc", params["longpc"], lamberta)
    latprjc = xml_node("latprjc", params["latprjc"], lamberta)
    feast = xml_node("feast", params["feast"], lamberta)
    fnorth = xml_node("fnorth", params["fnorth"], lamberta)
    return lamberta


def lambert_conformal_conic(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
     Lambert Conformal Conic projection

    stdparll = First standard parallel
    stdparl_2 = Second standard parallel (if exists)
    longcm = Longitude of Central Meridian
    latprjo = Latitude of Projection Origin
    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc Lambert Conformal Conic projection
    """
    lambertc = xml_node("lambertc")
    stdparll = xml_node("stdparll", params["stdparll"], lambertc)
    if params["stdparll_2"] != "Unknown":
        stdparll_2 = xml_node("stdparll", params["stdparll_2"], lambertc)

    for item in ["longcm", "latprjo", "feast", "fnorth"]:
        xml_node(item, params[item], lambertc)
    return lambertc


def mercator(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Equirectangular projection

    stdparll = First standard parallel
    longcm = Longitude of Central Meridian
    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc Mercator projection
    """
    mercator = xml_node("mercator")
    stdparll = xml_node("stdparll", params["stdparll"], mercator)
    longcm = xml_node("longcm", params["longcm"], mercator)
    feast = xml_node("feast", params["feast"], mercator)
    fnorth = xml_node("fnorth", params["fnorth"], mercator)
    return mercator


def modified_stereograhic_for_alaska(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
     Modified Stereographic for Alaska projection

    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc Modified Stereographic for Alaska projection
    """
    modsak = xml_node("modsak")
    feast = xml_node("feast", params["feast"], modsak)
    fnorth = xml_node("fnorth", params["fnorth"], modsak)
    return modsak


def miller_cylindrical(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Miller Cylindrical projection

    longcm = Longitude of Central Meridian
    feast = False Easting
    fnorth = False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    lxml nodes for fgdc Miller Cylindrical projection
    """
    miller = xml_node("miller")
    longcm = xml_node("longcm", params["longcm"], miller)
    feast = xml_node("feast", params["feast"], miller)
    fnorth = xml_node("fnorth", params["fnorth"], miller)
    return miller


###def oblique_mercator(params):
# how to handle oblique line azimuth (and dependent elements) OR oblique line point
# (and dependent elements)? - why does there need to be two occurrences of oblique line lat/long?


def orthographic(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Orthographic projection

    longpc = Longitude of Projection Center
    latprjc = Latitude of Projection Center
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Orthographic projection
    """
    orthogr = xml_node("orthogr")
    longpc = xml_node("longpc", params["longpc"], orthogr)
    latprjc = xml_node("latprjc", params["latprjc"], orthogr)
    feast = xml_node("feast", params["feast"], orthogr)
    fnorth = xml_node("fnorth", params["fnorth"], orthogr)
    return orthogr


def polar_stereographic(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Stereographic projection

    longpc = Longitude of Projection Center
    latprjc = Latitude of Projection Center
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Stereographic projection
    """
    polarst = xml_node("polarst")
    xml_node("svlong", params["svlong"], polarst)
    xml_node("longpc", params["longpc"], polarst)
    xml_node("latprjc", params["latprjc"], polarst)
    xml_node("feast", params["feast"], polarst)
    xml_node("fnorth", params["fnorth"], polarst)
    return polarst


def polyconic(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
     Polyconic projection

    longcm = Longitude of Central Meridian
    latprjc = Latitude of Projection Origin
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Polyconic projection
    """
    polycon = xml_node("polycon")
    longcm = xml_node("longcm", params["longcm"], polycon)
    latprjo = xml_node("latprjo", params["latprjo"], polycon)
    feast = xml_node("feast", params["feast"], polycon)
    fnorth = xml_node("fnorth", params["fnorth"], polycon)
    return polycon


def robinson(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Robinson projection

    longpc = Longitude of Projection Center
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Robinson projection
    """
    robinson = xml_node("robinson")
    longpc = xml_node("longpc", params["longpc"], robinson)
    feast = xml_node("feast", params["feast"], robinson)
    fnorth = xml_node("fnorth", params["fnorth"], robinson)
    return robinson


def sinusoidal(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Sinusoidal projection

    longcm = Longitude of Central Meridian
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Sinusoidal projection
    """
    sinusoid = xml_node("sinusoid")
    longcm = xml_node("longcm", params["longcm"], sinusoid)
    feast = xml_node("feast", params["feast"], sinusoid)
    fnorth = xml_node("fnorth", params["fnorth"], sinusoid)
    return sinusoid


def space_oblique_mercator(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Space Oblique Mercator projection

    landsat = Landsat Number
    pathnum = Path Number
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Space Oblique Mercator projection
    """
    spaceobq = xml_node("spaceobq")
    landsat = xml_node("landsat", params["landsat"], spaceobq)
    pathnum = xml_node("pathnum", params["pathnum"], spaceobq)
    feast = xml_node("feast", params["feast"], spaceobq)
    fnorth = xml_node("fnorth", params["fnorth"], spaceobq)
    return spaceobq


def stereographic(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Stereographic projection

    longpc = Longitude of Projection Center
    latprjc = Latitude of Projection Center
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Stereographic projection
    """
    stereo = xml_node("stereo")
    longpc = xml_node("longpc", params["longpc"], stereo)
    latprjc = xml_node("latprjc", params["latprjc"], stereo)
    feast = xml_node("feast", params["feast"], stereo)
    fnorth = xml_node("fnorth", params["fnorth"], stereo)
    return stereo


def transverse_mercator(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Transverse Mercator projection

    sfctrmer = Scale Factor at Central Meridian
    longcm = Longitude of Central Meridian
    latprjo = Latitude of Projection Origin
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Transverse Mercator projection
    """
    transmer = xml_node("transmer")
    sfctrmer = xml_node("sfctrmer", params["sfctrmer"], transmer)
    longcm = xml_node("longcm", params["longcm"], transmer)
    latprjo = xml_node("latprjo", params["latprjo"], transmer)
    feast = xml_node("feast", params["feast"], transmer)
    fnorth = xml_node("fnorth", params["fnorth"], transmer)
    return transmer


def van_der_grinten(params):
    """
    returns lxml nodes that contain projection parameters for fgdc
    Van der Grinten projection

    longcm = Longitude of Central Meridian
    feast = False Easting
    fnorth - False Northing

    Parameters
    ----------
    params : dictionary
            geospatial parameters returned from get_params

    Returns
    -------
    xml nodes for fgdc Van der Grinten projection
    """
    vdgrin = xml_node("vdgrin")
    longcm = xml_node("longcm", params["longcm"], vdgrin)
    feast = xml_node("feast", params["feast"], vdgrin)
    fnorth = xml_node("fnorth", params["fnorth"], vdgrin)
    return vdgrin


def utm(params):
    gridsys = xml_node("gridsys")
    gridsysn = xml_node(
        "gridsysn", text="Universal Transverse Mercator", parent_node=gridsys
    )

    utm_node = xml_node("utm", parent_node=gridsys)
    utmzone = xml_node("utmzone", text=params["utmzone"], parent_node=utm_node)

    transmer = transverse_mercator(params)
    utm_node.append(transmer)

    return gridsys


def spcs(params):

    gridsys = xml_node("gridsys")
    if "1983" in params["geogcs"]:
        gridsysn = xml_node(
            "gridsysn", text="State Plane Coordinate System 1983", parent_node=gridsys
        )
    else:
        gridsysn = xml_node(
            "gridsysn", text="State Plane Coordinate System 1927", parent_node=gridsys
        )

    spcs_node = xml_node("spcs", parent_node=gridsys)
    utmzone = xml_node("spcszone", text=params["spcszone"], parent_node=spcs_node)

    mapproj_node = mapproj(params)
    spcs_node.append(mapproj_node)

    return gridsys


def arc(params):

    gridsys = xml_node("gridsys")
    gridsysn = xml_node("gridsysn", text="ARC Coordinate System", parent_node=gridsys)

    arc_node = xml_node("arcsys", parent_node=gridsys)
    utmzone = xml_node("arczone", text=params["arczone"], parent_node=arc_node)

    mapproj_node = mapproj(params)
    arc_node.append(mapproj_node)

    return gridsys


def lookup_fdgc_projname(gdal_name, mapprojn=""):

    if gdal_name == "Stereographic" and "polar" in mapprojn.lower():
        gdal_name = "Polar_Stereographic"

    for k, v in PROJECTION_LOOKUP.items():
        if v["gdal_name"] == gdal_name:
            return k, v["function"]

    print("!" * 79)
    print("!" * 79)
    print("!" * 79)
    print("not handled ", gdal_name)
    print("!" * 79)
    print("!" * 79)
    print("!" * 79)
    return None, None  # this will blow up!


def lookup_shortname(shortname):
    for k, v in PROJECTION_LOOKUP.items():
        if v["shortname"] == shortname:
            return v
    return None


PROJECTION_LOOKUP = collections.OrderedDict()

PROJECTION_LOOKUP["Albers Conical Equal Area"] = {
    "shortname": "albers",
    "gdal_name": "Albers_Conic_Equal_Area",
    "function": albers_conic_equal_area,
    "elements": ["stdparll", "stdparll_2", "longcm", "latprjo", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Azimuthal Equidistant"] = {
    "shortname": "azimequi",
    "gdal_name": "Azimuthal_Equidistant",
    "function": azimuthal_equidistant,
    "elements": ["longcm", "latprjo", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Equidistant Conic"] = {
    "shortname": "equicon",
    "gdal_name": "Equidistant_Conic",
    "function": equidistant_conic,
    "elements": ["stdparll", "stdparll_2", "longcm", "latprjo", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Equirectangular"] = {
    "shortname": "equirect",
    "gdal_name": "Equirectangular",
    "function": equirectangular,
    "elements": ["stdparll", "longcm", "feast", "fnorth"],
}

PROJECTION_LOOKUP["General Vertical Near-sided Perspective"] = {
    "shortname": "gvnsp",
    "gdal_name": "General_Vertical_Near-sided_Perspective",
    "function": general_vertical_near_sided_perspective,
    "elements": ["heightpt", "longpc", "latprjc", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Gnomonic"] = {
    "shortname": "gnomonic",
    "gdal_name": "Gnomonic",
    "function": gnomonic,
    "elements": ["longpc", "latprjc", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Lambert Azimuthal Equal Area"] = {
    "shortname": "lamberta",
    "gdal_name": "Lambert_Azimuthal_Equal_Area",
    "function": lambert_azimuthal_equal_area,
    "elements": ["longpc", "latprjc", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Lambert Conformal Conic"] = {
    "shortname": "lambertc",
    "gdal_name": "Lambert_Conformal_Conic_2SP",
    "function": lambert_conformal_conic,
    "elements": ["stdparll", "stdparll_2", "longcm", "latprjo", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Mercator"] = {
    "shortname": "mercator",
    "gdal_name": "Mercator_2SP",
    "function": equirectangular,
    "elements": ["stdparll", "longcm", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Modified Stereographic for Alaska"] = {
    "shortname": "modsak",
    "gdal_name": "Modified_Stereographic_for_Alaska",
    "function": modified_stereograhic_for_alaska,
    "elements": ["feast", "fnorth"],
}

PROJECTION_LOOKUP["Miller Cylindrical"] = {
    "shortname": "miller",
    "gdal_name": "Miller_Cylindrical",
    "function": miller_cylindrical,
    "elements": ["longcm", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Orthographic"] = {
    "shortname": "orthogr",
    "gdal_name": "Orthographic",
    "function": orthographic,
    "elements": ["longpc", "latprjc", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Polar_Stereographic"] = {
    "shortname": "polarst",
    "gdal_name": "Polar_Stereographic",
    "function": polar_stereographic,
    "elements": ["svlong", "longpc", "latprjc", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Polyconic"] = {
    "shortname": "polycon",
    "gdal_name": "Polyconic",
    "function": polyconic,
    "elements": ["longcm", "latprjo", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Robinson"] = {
    "shortname": "robinson",
    "gdal_name": "Robinson",
    "function": robinson,
    "elements": ["longpc", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Sinusoidal"] = {
    "shortname": "sinusoid",
    "gdal_name": "Sinusoidal",
    "function": sinusoidal,
    "elements": ["longcm", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Space Oblique Mercator"] = {
    "shortname": "spaceobq",
    "gdal_name": " ",
    "function": space_oblique_mercator,
    "elements": ["landsat", "pathnum", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Stereographic"] = {
    "shortname": "stereo",
    "gdal_name": "World_Stereographic",
    "function": stereographic,
    "elements": ["longpc", "latprjc", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Transverse Mercator"] = {
    "shortname": "transmer",
    "gdal_name": " ",
    "function": transverse_mercator,
    "elements": ["sfctrmer", "longcm", "latprjo", "feast", "fnorth"],
}

PROJECTION_LOOKUP["Van der Grinten"] = {
    "shortname": "vdgrin",
    "gdal_name": " ",
    "function": van_der_grinten,
    "elements": ["longcm", "feast", "fnorth"],
}

PROJECTION_LOOKUP["undefined"] = {
    "shortname": "mapprojp",
    "gdal_name": "NA",
    "function": "NA",
    "elements": ["stdparll", "stdparll_2", "longcm", "latprjo", "feast", "fnorth"],
}


GRIDSYS_LOOKUP = collections.OrderedDict()

GRIDSYS_LOOKUP["Universal Transverse Mercator"] = {
    "shortname": "utm",
    "elements": ["utmzone"],
    "projection": "Transverse Mercator",
}
GRIDSYS_LOOKUP["Universal Polar Stereographic"] = {
    "shortname": "ups",
    "elements": ["upszone"],
    "projection": "Polar_Stereographic",
}
GRIDSYS_LOOKUP["State Plane Coordinate System 1927"] = {
    "shortname": "spcs",
    "elements": ["spcszone"],
    "projection": "Transverse Mercator",
}
GRIDSYS_LOOKUP["State Plane Coordinate System 1983"] = {
    "shortname": "spcs",
    "elements": ["spcszone"],
    "projection": "Transverse Mercator",
}
GRIDSYS_LOOKUP["ARC Coordinate System"] = {
    "shortname": "arcsys",
    "elements": ["arczone"],
    "projection": "Azimuthal Equidistant",
}
GRIDSYS_LOOKUP["other grid system"] = {
    "shortname": "othergrd",
    "elements": ["othergrd"],
    "projection": "Transverse Mercator",
}

DATUM_LOOKUP = {
    "North American Datum of 1927 (NAD 27)": {
        "ellips": "Clarke 1866",
        "semiaxis": "6378206.400000",
        "denflat": "294.978698",
    },
    "North American Datum of 1983 (NAD 83)": {
        "ellips": "Geodetic Reference System 1980",
        "semiaxis": "6378137.000000",
        "denflat": "298.257222",
    },
    "World Geodetic System 1984 (WGS 84)": {
        "ellips": "WGS_1984",
        "semiaxis": "6378137.000000",
        "denflat": "298.257224",
    },
}


def get_bounding(fname):
    """
    Return FGDC bounding element from provided espatial file

    Parameters
    ----------
    fname : name of the shp or tif file we'll be generating the bounding for

    Returns
    -------
    lxml element with FGDC Bounding
    """
    layer = get_layer(fname)
    extent = get_geographic_extent(layer)

    extent = format_bounding(extent)

    bounding = xml_node("bounding")
    westbc = xml_node("westbc", extent[0], bounding)
    eastbc = xml_node("eastbc", extent[1], bounding)
    northbc = xml_node("northbc", extent[2], bounding)
    southbc = xml_node("southbc", extent[3], bounding)

    return bounding


def num_sig_digits(f, min_num=4):
    """
    Determine the number of significant digits to display

    Parameters
    ----------
    f : float
        The number used to determine the appropriate number of digits to
        return
    min_num : int
            The minimum number of digits to return

    Returns
    -------
    int
    """
    try:
        if f > 0.9999:
            return min_num
        else:
            digit_list = list(str(f))[2:]
            first_nonzero = next(
                (i for i, x in enumerate(digit_list) if x != "0"), None
            )
            return first_nonzero + min_num
    except:
        return min_num


def format_bounding(extent):
    """
    convert to formated string strings with reasonable number of places

    Parameters
    ----------
    bounding : tuple
            (west, east, north, south)

    Returns :
        tuple : ("west", "east", "north", "south")
    -------

    """
    w, e, n, s = extent
    smallest_dim = min((e - w), (n - s))
    decimals = num_sig_digits(smallest_dim)
    return [
        "{num:.{decimals}f}".format(num=coord, decimals=decimals) for coord in extent
    ]


def get_spdoinfo(fname, feature_class=None):
    """
    Return FGDC bounding element from provided spatial file

    Parameters
    ----------
    fname : name of the shp or tif file we'll be generating the bounding for

    Returns
    -------
    lxml element with FGDC Bounding
    """
    if fname.endswith(".shp"):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataset = driver.Open(fname)
        layer = dataset.GetLayer()
        return vector_spdoinfo(layer)
    elif fname.endswith(".gdb"):
        driver = ogr.GetDriverByName("OpenFileGDB")
        gdb = driver.Open(fname, 0)
        layer = gdb.GetLayerByName(feature_class)
        return vector_spdoinfo(layer)
    elif fname.endswith(".las") or fname.endswith(".laz"):
        layer = laspy.open(fname)
        return las_spdoinfo(layer)
    elif fname.endswith(".gdb"):
        driver = ogr.GetDriverByName("OpenFileGDB")
        gdb = driver.Open(fname, 0)
        layer = gdb.GetLayerByName(feature_class)
        return vector_spdoinfo(layer)
    else:
        # it better be a raster
        data = gdal.Open(fname)
        return raster_spdoinfo(data)

    return None


def vector_spdoinfo(layer):
    """
    generate a fgdc Point Vector Object information element from a OGR layer
    Parameters
    ----------
    layer : ogr layer

    Returns
    -------
    lxml element
    """
    # introspect our layer to get the info we need
    feature_count = layer.GetFeatureCount()
    for geo in layer:
        geo_ref = geo.GetGeometryRef()
        geo_type = geo_ref.GetGeometryType()
        break

    # create the FGDC element
    spdoinfo = xml_node("spdoinfo")
    direct = xml_node("direct", text="Vector", parent_node=spdoinfo)

    ptvctinf = xml_node("ptvctinf", parent_node=spdoinfo)
    sdtsterm = xml_node("sdtsterm", parent_node=ptvctinf)

    if geo_type in [3, 6, 2003, 3003, 2006, 3006]:
        sdtstype = xml_node("sdtstype", text="G-polygon", parent_node=sdtsterm)
    elif geo_type in [2, 5, 2005, 3005]:
        sdtstype = xml_node("sdtstype", text="String", parent_node=sdtsterm)
    elif geo_type in [1, 4, 2001, 3001, 2004, 3004]:
        sdtstype = xml_node("sdtstype", text="Entity point", parent_node=sdtsterm)
    else:
        sdtstype = xml_node("sdtstype", text="Unknown", parent_node=sdtsterm)

    xml_node("ptvctcnt", text=feature_count, parent_node=sdtsterm)
    return spdoinfo


def raster_spdoinfo(data):
    """
    generate a fgdc Raster Object information element from a gdal dataset
    Parameters
    ----------
    data : gdal dataset

    Returns
    -------
    lxml element
    """
    # introspect our data to get the info we need
    raster_type = "Grid Cell"  # This is the most probable answer
    cols = data.RasterXSize
    rows = data.RasterYSize
    bands = data.RasterCount

    # create the FGDC element
    spdoinfo = xml_node("spdoinfo")
    direct = xml_node("direct", text="Raster", parent_node=spdoinfo)
    rastinfo = xml_node("rastinfo", parent_node=spdoinfo)

    rasttype = xml_node("rasttype", text=raster_type, parent_node=rastinfo)
    rowcount = xml_node("rowcount", text=rows, parent_node=rastinfo)
    colcount = xml_node("colcount", text=cols, parent_node=rastinfo)
    vrtcount = xml_node("vrtcount", text=bands, parent_node=rastinfo)

    return spdoinfo

def las_spdoinfo(layer):
    """
    generate a fgdc Point Vector Object information element from a OGR layer
    Parameters
    ----------
    layer : ogr layer

    Returns
    -------
    lxml element
    """
    # introspect our layer to get the info we need
    feature_count = layer.header.point_count

    # create the FGDC element
    spdoinfo = xml_node("spdoinfo")
    direct = xml_node("direct", text="Vector", parent_node=spdoinfo)

    ptvctinf = xml_node("ptvctinf", parent_node=spdoinfo)
    sdtsterm = xml_node("sdtsterm", parent_node=ptvctinf)
    sdtstype = xml_node("sdtstype", text="Point", parent_node=sdtsterm)
    xml_node("ptvctcnt", text=feature_count, parent_node=sdtsterm)

    return spdoinfo

def band_to_df(band):
    """
    Creates a dataframe with one column (Value) and two rows with the bands
    min and max value

    Parameters
    ----------
    band : osgeo raster band object

    Returns
    -------
    pandas dataframe
    """
    cols = ["Value"]
    stats = band.GetStatistics(True, True)
    rows = [[stats[0]], [stats[1]]]
    df = pd.DataFrame.from_records(rows, columns=cols)
    df["Value"] = df["Value"].astype(float)
    return df


def get_band_count(fname):
    raster = get_layer(fname)
    return raster.RasterCount


def rat_to_df(rat):
    """
    converts a raster attribute table into a pandas dataframe

    Parameters
    ----------
    rat : osgeo GDALRasterAttributeTable

    Returns
    -------
        pandas dataframe
    """
    icolcount = rat.GetColumnCount()
    cols = []
    for icol in range(icolcount):
        cols.append(rat.GetNameOfCol(icol))

    irowcount = rat.GetRowCount()
    rows = []
    for irow in range(irowcount):
        vals = []
        for icol in range(icolcount):
            itype = rat.GetTypeOfCol(icol)
            if itype == gdal.GFT_Integer:
                value = "%s" % rat.GetValueAsInt(irow, icol)
            elif itype == gdal.GFT_Real:
                value = "%.16g" % rat.GetValueAsDouble(irow, icol)
            else:
                value = "%s" % rat.GetValueAsString(irow, icol)
            vals.append(value)
        rows.append(vals)

    df = pd.DataFrame.from_records(rows, columns=cols)
    for icol in range(icolcount):
        col_name = rat.GetNameOfCol(icol)
        itype = rat.GetTypeOfCol(icol)
        if itype == gdal.GFT_Integer:
            df[col_name] = df[col_name].astype(int)
        elif itype == gdal.GFT_Real:
            df[col_name] = df[col_name].astype(float)
        else:
            df[col_name] = df[col_name].astype(str)

    return df


def get_raster_attribute_table(fname):
    """
    returns the raster attribute table in a pandas dataframe format
    Parameters
    ----------
    fname : str
            file name of the raster we'll be using

    Returns
    -------
    pandas dataframe
    """
    raster = get_layer(fname)
    band = raster.GetRasterBand(1)
    rat = band.GetDefaultRAT()

    if rat != None:
        df = rat_to_df(rat)
        if not df.columns == ["Histogram"]:
            return df

    # check for a sidecar dbf vat
    vatdbf = fname + ".vat.dbf"
    if os.path.exists(vatdbf):
        vat = data_io.read_dbf(vatdbf)
        if "OID" not in vat.columns:
            vat.insert(0, "OID", range(0, len(vat)))
        return vat.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    else:
        dfs = []
        for band_num in range(1, raster.RasterCount + 1):
            band = raster.GetRasterBand(band_num)
            dfs.append(band_to_df(band))
        df = pd.concat(dfs)

        return df


if __name__ == "__main__":
    fname = r"wgs84.shp"
    get_spref(fname)
