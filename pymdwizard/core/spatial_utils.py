#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module provide a variety of spatial introspection functions.
Produces FGDC spatial elements from spatial data sets


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import os
import sys
import collections
import math

# Non-standard python libraries.
try:
    import numpy as np
    import pandas as pd

    # Address warning: Warning 3: Cannot find header.dxf (GDAL_DATA is not
    # defined). Include before importing geopandas and fiona.
    os.environ["GDAL_DATA"] = os.path.join(
        f"{os.sep}".join(sys.executable.split(os.sep)[:-1]),
        "Library", "share", "gdal")
    from osgeo import gdal
    from osgeo import osr
    from osgeo import ogr

    gdal.UseExceptions()
    gdal.AllRegister()
    use_gdal = True

    import laspy
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core.xml_utils import xml_node
    from pymdwizard.core import (utils, data_io)
except ImportError as err:
    raise ImportError(err, __file__)


def set_local_gdal_data():
    """
    Description:
        Sets the environment variable for the local GDAL instance path.

    Returns:
        None
    """

    # Get the installation directory of Python.
    python_root = utils.get_install_dname("python")

    # Construct the path to the GDAL data directory.
    gdal_data = os.path.join(python_root, "Library", "share", "gdal")

    # Set the GDAL_DATA environment variable.
    os.environ["GDAL_DATA"] = gdal_data


def _get_las_extent(fh):
    """
    Description:
        Extracts the projected extent from a LAS file header.
        Returns the coordinates in the format (min_x, max_x, min_y, max_y).

    Args:
        fh (LAS file handle): A file handle that provides access to the LAS
            file header.

    Returns:
        tuple: A tuple containing the upper left x-coordinate (min_x),
            lower right x-coordinate (max_x), lower right y-coordinate
            (min_y), and upper left y-coordinate (max_y) of the LAS
            file extent.
    """

    # Access the header of the LAS file
    header = fh.header

    # Extract the x and y coordinates from the header.
    ulx = header.x_min
    lrx = header.x_max
    uly = header.y_max
    lry = header.y_min

    return ulx, lrx, lry, uly


def _get_raster_extent(src):
    """
    Description:
        Extracts the projected extent from a raster dataset.
        Returns the coordinates in the format (min_x, max_x, min_y, max_y).

    Args:
        src (gdal raster): The raster dataset from which to extract the extent.

    Returns:
        tuple: A tuple containing the upper left x-coordinate (min_x),
            lower right x-coordinate (max_x), lower right y-coordinate
            (min_y), and upper left y-coordinate (max_y) of the raster
            dataset extent.
    """

    # Get the geotransform parameters from the raster dataset.
    ulx, xres, xskew, uly, yskew, yres = src.GetGeoTransform()

    # Calculate the lower right x and y coordinates.
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)

    return ulx, lrx, lry, uly


def get_extent(layer):
    """
    Description:
        Returns the projected extent from an OGR layer or GDAL dataset.
        The extent is returned in the format (min_x, max_x, min_y, max_y).

    Args:
        layer (ogr layer or gdal dataset): The layer or dataset from which to
            extract the extent.

    Returns:
        tuple or None: A tuple containing the extent coordinates (min_x, max_x,
            min_y, max_y) if found; otherwise, returns None.
    """

    # Attempt to retrieve extent from the layer using GetExtent()
    try:
        return layer.GetExtent()
    except Exception:
        pass

    # Attempt to retrieve extent using a LAS extent function
    try:
        return _get_las_extent(layer)
    except Exception:
        pass

    # Attempt to retrieve extent using a raster extent function
    try:
        return _get_raster_extent(layer)
    except Exception:
        pass


def get_geographic_extent(layer):
    """
    Description:
        Returns the extent in geographic (latitude, longitude) coordinates.

    Args:
        layer (ogr layer or gdal dataset): The layer or dataset from which to
            extract the geographic extent.

    Returns:
        tuple: A tuple containing the westernmost, easternmost, southernmost,
            and northernmost coordinates (west, east, south, north).
    """

    # Get the extent in projected coordinates.
    min_x, max_x, min_y, max_y = get_extent(layer)

    # Retrieve the spatial reference from the layer.
    srs = get_ref(layer)
    srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

    # Clone the geographic coordinate system and define axis mapping.
    # Get the body (planet or moon) from the projection definition
    # removes the lock-in to EPSG:4326 (WGS84)
    target = srs.CloneGeogCS()
    target.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

    # Attempt to extract spatial reference information.
    try:
        spatialRef = layer.GetSpatialRef()
        spatialRef.ExportToProj4()
        spatialRef.AutoIdentifyEPSG()
        spref = spatialRef.GetAuthorityCode(None)
    except:
        pass

    # Calculate geographic bounds using the extent and reference systems.
    west, east, south, north = \
        calculate_max_bounds(min_x, max_x, min_y, max_y, srs, target)

    return west, east, south, north


def calculate_max_bounds(min_x, max_x, min_y, max_y, src_srs, target_srs):
    """
    Description:
        Calculates maximum east, minimum west, maximum north, and minimum
        south coordinates after transforming points from the source SRS to the
        target SRS.

    Args:
        min_x (float): The minimum x-coordinate of the extent.
        max_x (float): The maximum x-coordinate of the extent.
        min_y (float): The minimum y-coordinate of the extent.
        max_y (float): The maximum y-coordinate of the extent.
        src_srs (spatial reference): The source spatial reference system.
        target_srs (spatial reference): The target spatial reference system.

    Returns:
        tuple: A tuple of calculated bounds in the format
            (min_west, max_east, max_north, min_south).
    """

    # Define the number of interpolation steps for calculation
    steps = 10

    # Initialize the values for each direction
    max_east = -float('inf')
    min_west = float('inf')
    max_north = -float('inf')
    min_south = float('inf')

    # Calculate max_east and min_west.
    for step in range(steps + 1):
        cur_north = min_y + step * ((max_y - min_y) / steps)

        # Max East
        transformed_east = transform_point((max_x, cur_north),
                                           src_srs, target_srs)
        if transformed_east[0] > max_east:
            max_east = transformed_east[0]

        # Min West
        transformed_west = transform_point((min_x, cur_north),
                                           src_srs, target_srs)
        if transformed_west[0] < min_west:
            min_west = transformed_west[0]

    # Calculate max_north and min_south
    for step in range(steps + 1):
        cur_east = min_x + step * ((max_x - min_x) / steps)

        # Max North
        transformed_north = transform_point((cur_east, max_y),
                                            src_srs, target_srs)
        if transformed_north[1] > max_north:
            max_north = transformed_north[1]

        # Min South
        transformed_south = transform_point((cur_east, min_y),
                                            src_srs, target_srs)
        if transformed_south[1] < min_south:
            min_south = transformed_south[1]

    return min_west, max_east, max_north, min_south


def get_ref(layer):
    """
    Description:
        Returns the OSR geospatial reference from an OGR layer or GDAL dataset.

    Args:
        layer (ogr layer or gdal dataset): The layer or dataset from which to
            extract the geospatial reference.

    Returns:
        osr.SpatialReference: An OSR geospatial reference object if available;
            otherwise, None.
    """

    # Initialize WKT variable to hold the Well-Known Text representation.
    wkt = None

    # Attempt to get the WKT from various methods
    try:
        wkt = layer.GetProjection()
    except Exception:
        pass

    # Parse CRS from header
    try:
        wkt = layer.header.parse_crs().to_wkt()
    except Exception:
        pass

    # Get spatial reference WKT.
    try:
        wkt = layer.GetSpatialRef().ExportToWkt()
    except Exception:
        pass

    # Return the OSR SpatialReference object created from the WKT, or None.
    if wkt is not None:
        return osr.SpatialReference(wkt=wkt)

    return osr.SpatialReference(wkt=wkt)


def get_latlong_res(extent):
    """
    Description:
        Calculates the latitudinal and longitudinal resolution for a given
        geographic extent based on the WGS 84 spheroid model.

    Args:
        extent : tuple
            A tuple containing the minimum longitude, maximum longitude,
            minimum latitude, and maximum latitude of the geographic area.

    Returns:
        tuple
            A tuple containing the latitudinal and longitudinal resolutions
            as strings formatted to 10 decimal places.

    Notes:
        D. Ignizio: This function is a modified approach to calculating
        latitudinal and longitudinal resolution in a GCS.
        Use in lieu of Vincenty's algorithm due to complexity/issues with
        incorrect results.
        The formula calculates values against the WGS 84 spheroid.
        The mid-point of the latitudinal extent of the dataset is used to
        calculate values, as they change depending on where on the globe
        we are considering.
    """

    # Unpack the extent coordinates.
    min_lon, max_lon, min_lat, max_lat = extent

    # Calculate mid-latitude position while handling the hemisphere.
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

    # Length of 1 degree of Latitude in kilometers
    x = mid_lat
    len1_degree_lat = (
        (-3e-06 * pow(x, 3)) + (0.0005 * pow(x, 2)) - (0.0013 * x) + 110.57
    )
    len1_minute_lat = len1_degree_lat / 60
    len1_second_lat = len1_minute_lat / 60

    # Constants for calculations
    data_scale = 24000  # Scale factor for the resolution
    dig_precision = 0.001  # Digital precision factor

    # Calculate latitudinal resolution.
    lat_res = float(
        (1 / len1_second_lat) * (1 / 3280.84) * data_scale * (1.0 / 12) *
        dig_precision
    )
    latlat_reses = str(format(lat_res, ".10f"))

    # Length of 1 degree of Longitude in kilometers @ Latitude(y) on the globe.
    # y = 7E-05x^3 - 0.0203x^2 + 0.0572x + 111.24

    # Length of 1 degree of Longitude in kilometers.
    len1_degree_long = (
        (7e-05 * pow(x, 3)) - (0.0203 * pow(x, 2)) + (0.0572 * x) + 111.24
    )
    len1_minute_long = len1_degree_long / 60
    len1_second_long = len1_minute_long / 60

    # Calculate longitudinal resolution
    long_res = float(
        (1 / len1_second_long) * (1 / 3280.84) * data_scale * (1.0 / 12) *
        dig_precision
    )
    long_res = str(format(long_res, ".10f"))

    return latlat_reses, long_res


def get_abs_resolution(src, params):
    """
    Description:
        Calculates the absolute resolution in both the x and y directions
        for a given source. It distinguishes between raster and vector data.

    Args:
        src (object): The source object from which to obtain the geographic
            transform.
        params (dict): A dictionary that contains parameters needed for
            resolution calculations and will be updated with results.

    Returns:
        None

    Notes:
        The minimum difference between X (abscissa) and Y (ordinate) values in
        the planar data set.

        The values usually indicate the ?fuzzy tolerance? or ?clustering?
        setting that establishes the minimum distance at which two points will
        NOT be automatically converged by the data collection device (digitizer,
        GPS, etc.). NOTE: units of measures are provided under element Planar
        Distance Units.

        Raster data: Abscissa/ordinate res equals cell resolution
        Vector data: Abscissa/ordinate res is the smallest measurable distance
    """

    try:
        # Attempt to obtain the geo-transform, which works for raster data.
        xform = src.GetGeoTransform()
        params["absres"] = math.fabs(xform[1])
        params["latres"] = math.fabs(xform[1])
        params["ordres"] = math.fabs(xform[5])
        params["longres"] = math.fabs(xform[5])
    except:
        # Calculate resolutions based on projection parameters for vector data.
        if params["mapprojn"] != "Unknown":
            data_scale = 24000
            dig_precision = 0.001

            # Determine the unit of measure and calculate the resolutions.
            # Industry-standard digitizer precision of 0.001"
            if params["plandu"].lower() == "feet":
                params["absres"] = str(
                    float(data_scale) * float(dig_precision) / 12.0)
                params["ordres"] = str(
                    float(data_scale) * float(dig_precision) / 12.0)
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
            # If projection is unknown, use existing lat/long resolutions.
            params["absres"] = params["latres"]
            params["ordres"] = params["longres"]


def get_params(layer):
    """
    Description:
        Retrieves various parameters from a given geographic layer and outputs
        them in a structured dictionary.

    Args:
        layer (ogr layer or gdal dataset): The layer from which to extract
            parameters.

    Returns:
        dict: A dictionary containing various parameters related to spatial
            reference and geographic characteristics of the layer.
    """

    # Get spatial reference and extent information from the layer.
    ref = get_ref(layer)
    projected_extent = get_extent(layer)
    geographic_extent = get_geographic_extent(layer)

    params = {}

    # Get latitudinal and longitudinal resolutions.
    params["latres"], params["longres"] = get_latlong_res(geographic_extent)
    params["latres"], params["longres"] = str(
        params["latres"]), str(params["longres"])

    params["geogunit"] = "Decimal seconds"  # always use Decimal Seconds
    params["mapprojn"] = ref.GetAttrValue("projcs")
    params["projection_name"] = ref.GetAttrValue("projection")
    params["geogcs"] = ref.GetAttrValue("geogcs")

    # Get projection parameters and ensure all values are strings.
    params["stdparll"] = str(ref.GetProjParm(osr.SRS_PP_STANDARD_PARALLEL_1))
    params["stdparll_2"] = str(ref.GetProjParm(osr.SRS_PP_STANDARD_PARALLEL_2))
    params["longcm"] = str(ref.GetProjParm(osr.SRS_PP_CENTRAL_MERIDIAN))
    params["latprjo"] = str(ref.GetProjParm(osr.SRS_PP_LATITUDE_OF_ORIGIN))
    params["feast"] = str(ref.GetProjParm(osr.SRS_PP_FALSE_EASTING))
    params["fnorth"] = str(ref.GetProjParm(osr.SRS_PP_FALSE_NORTHING))
    params["sfequat"] = str(ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR))
    params["heightpt"] = str(ref.GetProjParm(
        osr.SRS_PP_PERSPECTIVE_POINT_HEIGHT))
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

    # Default unknown values for several parameters.
    params["distres"] = "Unknown"
    params["bearres"] = "Unknown"
    params["bearunit"] = "Unknown"
    params["bearrefd"] = "Unknown"
    params["bearrefm"] = "Unknown"
    params["plandu"] = ref.GetLinearUnitsName()

    # Set various local properties to "Unknown" and populate those that data
    # retain.
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

    # Initialize unknown values if params are None.
    for k in params:
        if params[k] is None:
            params[k] = "Unknown"

    # Get absolute resolution parameters.
    get_abs_resolution(layer, params)

    # SPCS_Zone determination
    if (params["mapprojn"] != None and
            "stateplane" in params["mapprojn"].lower()):
        parts = params["mapprojn"].split("_")
        params["spcszone"] = str(parts[parts.index("FIPS") + 1])
    else:
        params["spcszone"] = "Unknown"

    # ARC_Zone determination.
    if (params["mapprojn"] != None and
            "_arc_system" in params["mapprojn"].lower()):
        parts = params["mapprojn"].split("_")
        params["arczone"] = str(parts[-1])
    else:
        params["arczone"] = "Unknown"

    # PCS_Units determination.
    params["upzone"] = "Unknown"

    return params


def transform_point(xy, from_srs, to_srs):
    """
    Description:
        Transforms a point from one spatial reference system (SRS) to another.

    Args:
        xy (tuple): A tuple containing the x and y coordinates (x, y) to
            transform.
        from_srs (osr.SpatialReference): The source spatial reference system of
            the coordinates.
        to_srs (osr.SpatialReference): The target spatial reference system to
            which the coordinates need to be transformed.

    Returns:
        tuple:  tuple containing the transformed coordinates (x, y).
    """

    # Create a coordinate transformation object using the provided SRS.
    coord_xform = osr.CoordinateTransformation(from_srs, to_srs)

    # Round the coordinates to 8 decimal places for precision.
    y_round = round(xy[1], 8)
    x_round = round(xy[0], 8)

    # Transform the point using the coordinate transformation object.
    results = coord_xform.TransformPoint(x_round, y_round)

    return results[0], results[1]


def get_layer(fname, feature_class=None):
    """
    Description:
        Type-agnostic function for opening a file without specifying its type.

    Args:
        fname (str): The filename and path to the file to open.
        feature_class (str, optional): If the fname is a file geodatabase, then
            the feature class name is required.

    Returns:
        Either a shapefile, feature class (ESRI File GeoDatabase), or lidar
        (.las) object depending on the input file type. If these are not found
        a raster dataset is returned (GDAL Dataset).
    """

    # Why are we setting global ???????????????????????????????????????????????????????????????????
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
    elif fname.endswith(".las") or fname.endswith(".laz"):  # ??????????????????????? why not global fh
        fh = laspy.open(fname)
        return fh
    else:
        # it better be a raster
        return gdal.Open(fname)


def get_spref(fname, feature_class=None):
    """
    Description:
        Returns the FGDC XML element with the spatial reference extracted
        from a dataset.

    Args:
        fname (str): The filename and path to the file to open.
        feature_class (str, optional): If the fname is a file geodatabase,
            then the feature class name is required.

    Returns:
        ogr spatial reference object: A spatial reference object expressed in
            the FGDC XML format.
    """

    # Retrieve the layer from the specified filename and feature class.
    layer = get_layer(fname, feature_class=feature_class)

    # Extract parameters related to the spatial reference.
    params = get_params(layer)

    # Create the root spref XML node.
    spref = xml_node("spref")
    horizsys = xml_node("horizsys", parent_node=spref)

    # Determine if the projection is unknown, and append corresponding nodes.
    if params["mapprojn"] == "Unknown":
        # If the projection is unknown, append geographic node.
        geographic_node = geographic(params)
        horizsys.append(geographic_node)
    else:
        # If projection is known, append planar node.
        planar_node = planar(params)
        horizsys.append(planar_node)

    # Append the geodetic node to the horizontal system node.
    geodetic_node = geodetic(params)
    horizsys.append(geodetic_node)

    return spref


def geographic(params):
    """
    Description:
        Creates an FGDC <geograph> XML element using the provided parameters.

    Args:
        params (dict): A dictionary containing geographical parameters such as
            latitudinal resolution, longitudinal resolution, and geographic
            unit.

    Returns:
        xml_node: An FGDC <geograph> XML element populated with the relevant
            geographic parameters.
    """

    # Create the root <geograph> XML node.
    geograph = xml_node("geograph")

    # Create and append latitudinal and longitudinal resolution nodes.
    latres = xml_node("latres", params["latres"], geograph)
    longres = xml_node("longres", params["longres"], geograph)

    # Create and append geographic unit node.
    geounit = xml_node("geogunit", params["geogunit"], geograph)

    return geograph


def mapproj(params):
    """
    Description:
        Creates an FGDC <mapproj> XML element using the specified parameters.

    Args:
        params (dict): A dictionary of parameters which includes projection
            details such as projection name and map projection name.

    Returns:
        xml_node: An FGDC <mapproj> XML element populated with projection
            information.
    """

    # Create the root <mapproj> XML node.
    mapproj_node = xml_node("mapproj")

    # Lookup the FGDC projection name and associated function.
    fgdc_name, function = lookup_fdgc_projname(
        params["projection_name"], params["mapprojn"]
    )
    if fgdc_name is None:
        # Default to the provided projection name and create unknown projection
        # node.
        fgdc_name = params["projection_name"]
        prj_node = unknown_projection(params)
    else:
        # Call the function associated with the found FGDC projection name.
        prj_node = function(params)

    # Create the <mapprojn> node with the FGDC name and attach it to the parent.
    mapprojn = xml_node("mapprojn", text=fgdc_name,
                        parent_node=mapproj_node)
    mapproj_node.append(prj_node)

    return mapproj_node


def planar(params):
    """
    Description:
        Creates an FGDC <planar> XML element using the provided parameters.

    Args:
        params (dict): A dictionary of parameters, including zone information
            and other mapping details.

    Returns:
        xml_node: An FGDC <planar> XML element populated with relevant planar
            projection information.
    """

    # Create the root <planar> XML node.
    planar = xml_node("planar")

    # Determine the appropriate top node based on zone information.
    if params["utmzone"] != "Unknown":
        top_node = utm(params)
    elif params["spcszone"] != "Unknown":
        top_node = spcs(params)
    elif params["arczone"] != "Unknown":
        top_node = arc(params)
    elif params["mapprojn"] != "Unknown":
        top_node = mapproj(params)
    else:
        top_node = None  # Default case if no zone information is found

    # Append the determined top node to the <planar> node
    if top_node:  # Only append if a top_node was determined
        planar.append(top_node)

    # Create child nodes within the <planar> structure.
    planci = xml_node("planci", parent_node=planar)
    plance = xml_node("plance", text=params["plance"], parent_node=planci)
    coordrep = xml_node("coordrep", parent_node=planci)

    # Append absolute and ordinate resolution nodes.
    absres = xml_node("absres", text=params["absres"],
                      parent_node=coordrep)
    ordres = xml_node("ordres", text=params["ordres"],
                      parent_node=coordrep)

    # Append planar units information.
    plandu = xml_node("plandu", text=params["plandu"], parent_node=planci)

    return planar


def geodetic(params):
    """
    Description:
        Creates an FGDC <geodetic> XML element using the provided parameters.

    Args:
        params (dict): A dictionary containing geodetic parameters such as
            horizontal datum, spheroid, semi-major axis, and flattening.

    Returns:
        xml_node: An FGDC <geodetic> XML element populated with the relevant
            geodetic parameters.
    """

    # Create the root <geodetic> XML node.
    geodetic = xml_node("geodetic")

    # Append child nodes for each geodetic parameter.
    xml_node("horizdn", params["horizdn"], geodetic)
    xml_node("ellips", params["ellips"], geodetic)
    xml_node("semiaxis", params["semiaxis"], geodetic)
    xml_node("denflat", params["denflat"], geodetic)

    return geodetic


def albers_conic_equal_area(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for FGDC
        Albers Conic Equal Area projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for FGDC Albers Conic Equal Area projection
            that contain projection parameters for fgdc.

    Notes:
        stdparll = First standard parallel
        stdparl_2 = Second standard parallel (if exists)
        longcm = Longitude of Central Meridian
        latprjo = Latitude of Projection Origin
        feast = False Easting
        fnorth = False Northing
    """

    # Create the root <albers> XML node.
    albers = xml_node("albers")

    # Append the first standard parallel.
    stdparll = xml_node("stdparll", params["stdparll"], albers)

    # Append the second standard parallel if it exists.
    if params["stdparll_2"]:
        stdparll_2 = xml_node("stdparll", params["stdparll_2"], albers)

    # Append additional projection parameters to the <albers> node.
    for item in ["longcm", "latprjo", "feast", "fnorth"]:
        xml_node(item, params[item], albers)

    return albers


def azimuthal_equidistant(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Azimuthal Equidistant projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Azimuthal Equidistant projection.
    """

    # This section should probably be handled in a different function?
    # planar = xml_node("planar")
    # mapproj = xml_node("mapproj", parent_node=planar)
    # mapprojn = xml_node("mapprojn", params["mapprojn"], mapproj)

    # Create the root <azimequi> XML node for the projection.
    azimequi = xml_node("azimequi")

    # Append the longitude and latitude of the projection center to the
    # <azimequi> node.
    longcm = xml_node("longcm", params["longcm"], azimequi)
    latprjo = xml_node("latprjo", params["latprjo"], azimequi)

    # Append false easting and northing value to the <azimequi> node.
    feast = xml_node("feast", params["feast"], azimequi)
    fnorth = xml_node("fnorth", params["fnorth"], azimequi)

    return azimequi


def equidistant_conic(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Equidistant Conic projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Equidistant Conic projection.

    Notes:
        stdparll = First standard parallel
        stdparl_2 = Second standard parallel (if exists)
        longcm = Longitude of Central Meridian
        latprjo = Latitude of Projection Origin
        feast = False Easting
        fnorth = False Northing
    """

    # Create the root <equicon> XML node for the Equidistant Conic projection.
    equicon = xml_node("equicon")

    # Append the first standard parallel.
    stdparll = xml_node("stdparll", params["stdparll"], equicon)

    # Append the second standard parallel if it is defined.
    if params["stdparll_2"] != "Unknown":
        stdparll_2 = xml_node("stdparll", params["stdparll_2"], equicon)

    # Append additional projection parameters to the <equicon> node.
    for item in ["longcm", "latprjo", "feast", "fnorth"]:
        xml_node(item, params[item], equicon)

    return equicon


def unknown_projection(params):
    """
    Description:
        Creates an XML node for an unknown map projection based on the
        provided parameters.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: An XML node representing the unknown projection parameters.
    """

    # Create the root <mapprojp> XML node for the unknown projection.
    mapprojp = xml_node("mapprojp")

    # Append the first standard parallel if defined.
    if params["stdparll"] != "Unknown":
        stdparll = xml_node("stdparll", params["stdparll"], mapprojp)

    # Append the second standard parallel if defined.
    if params["stdparll_2"] != "Unknown":
        stdparll_2 = xml_node("stdparll", params["stdparll_2"], mapprojp)

    # List of additional parameters to be appended to the <mapprojp> node
    projection_keys = [
        "longcm", "latprjo", "feast", "fnorth", "sfequat",
        "heightpt", "longpc", "latprjc", "sfctrlin",
        "obqlazim", "azimangl", "azimptl"
    ]

    # Iterate through the keys and create XML nodes for defined parameters.
    for k in projection_keys:
        # Check if the parameter is not "Unknown" before appending
        if params[k] not in ["Unknown", "unknown"]:
            xml_node(k, params[k], mapprojp)

    return mapprojp


def equirectangular(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Equirectangular projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Equirectangular projection.
    """

    # Create the root <equirect> XML node for Equirectangular projection.
    equirect = xml_node("equirect")

    # Append the first standard parallel to the <equirect> node.
    stdparll = xml_node("stdparll", params["stdparll"], equirect)

    # Append the longitude of the central meridian.
    longcm = xml_node("longcm", params["longcm"], equirect)

    # Append false easting and false northing values.
    feast = xml_node("feast", params["feast"], equirect)
    fnorth = xml_node("fnorth", params["fnorth"], equirect)

    return equirect


def general_vertical_near_sided_perspective(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        General Vertical Near-sided Perspective projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC General Vertical Near-sided
            Perspective projection.
    """

    # Create the root <gvnsp> XML node for the projection.
    gvnsp = xml_node("gvnsp")

    # Append the height of perspective point above surface to the <gvnsp> node.
    heightpt = xml_node("heightpt", params["heightpt"], gvnsp)

    # Append the longitude and latitude of the projection center to the
    # <gvnsp> node.
    longpc = xml_node("longpc", params["longpc"], gvnsp)
    latprjc = xml_node("latprjc", params["latprjc"], gvnsp)

    # Append false easting and northing value to the <gvnsp> node.
    feast = xml_node("feast", params["feast"], gvnsp)
    fnorth = xml_node("fnorth", params["fnorth"], gvnsp)

    return gvnsp


def gnomonic(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Gnomonic projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Gnomonic projection.
    """

    # Create the root <gnomonic> XML node for the projection.
    gnomonic = xml_node("gnomonic")

    # Append the longitude and latitude of the projection center to the
    # <gnomonic> node.
    longpc = xml_node("longpc", params["longpc"], gnomonic)
    latprjc = xml_node("latprjc", params["latprjc"], gnomonic)

    # Append false easting and northing value to the <gnomonic> node.
    feast = xml_node("feast", params["feast"], gnomonic)
    fnorth = xml_node("fnorth", params["fnorth"], gnomonic)

    return gnomonic


def lambert_azimuthal_equal_area(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Lambert Azimuthal Equal Area projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: XML nodes for the FGDC Lambert Azimuthal Equal Area
            projection.
    """

    # Create the root <lamberta> XML node for the projection.
    lamberta = xml_node("lamberta")

    # Append the longitude and latitude of the projection center to the
    # <lamberta> node.
    longpc = xml_node("longpc", params["longpc"], lamberta)
    latprjc = xml_node("latprjc", params["latprjc"], lamberta)

    # Append false easting and northing value to the <lamberta> node.
    feast = xml_node("feast", params["feast"], lamberta)
    fnorth = xml_node("fnorth", params["fnorth"], lamberta)

    return lamberta


def lambert_conformal_conic(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Lambert Conformal Conic projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Lambert Conformal Conic projection.

    Notes:
        stdparll = First standard parallel
        stdparl_2 = Second standard parallel (if exists)
        longcm = Longitude of Central Meridian
        latprjo = Latitude of Projection Origin
        feast = False Easting
        fnorth = False Northing
    """

    # Create the root <lambertc> XML node for the projection.
    lambertc = xml_node("lambertc")

    # Append the first standard parallel to the <lambertc> node.
    stdparll = xml_node("stdparll", params["stdparll"], lambertc)

    # Append the second standard parallel if it is defined.
    if params["stdparll_2"] != "Unknown":
        stdparll_2 = xml_node("stdparll", params["stdparll_2"], lambertc)

    # Append additional projection parameters to the <lambertc> node.
    for item in ["longcm", "latprjo", "feast", "fnorth"]:
        xml_node(item, params[item], lambertc)

    return lambertc


def mercator(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Mercator projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Mercator projection.
    """

    # Create the root <mercator> XML node for the projection.
    mercator = xml_node("mercator")

    # Append the first standard parallel to the <mercator> node.
    stdparll = xml_node("stdparll", params["stdparll"], mercator)

    # Append the longitude of the central meridian.
    longcm = xml_node("longcm", params["longcm"], mercator)

    # Append false easting and northing.
    feast = xml_node("feast", params["feast"], mercator)
    fnorth = xml_node("fnorth", params["fnorth"], mercator)

    return mercator


def modified_stereograhic_for_alaska(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Modified Stereographic projection for Alaska.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Modified Stereographic for Alaska
            projection.
    """

    # Create the root <modsak> XML node for the projection.
    modsak = xml_node("modsak")

    # Append false easting and northing value to the <modsak> node.
    feast = xml_node("feast", params["feast"], modsak)
    fnorth = xml_node("fnorth", params["fnorth"], modsak)

    return modsak


def miller_cylindrical(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Miller Cylindrical projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Miller Cylindrical projection.
    """

    # Create the root <miller> XML node for the projection.
    miller = xml_node("miller")

    # Append the longitude of the central meridian to the <miller> node.
    longcm = xml_node("longcm", params["longcm"], miller)

    # Append false easting and northing value to the <miller> node.
    feast = xml_node("feast", params["feast"], miller)
    fnorth = xml_node("fnorth", params["fnorth"], miller)

    return miller


def oblique_mercator(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Oblique mercator projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Miller Oblique mercator.

    Notes:
        Do not know how to handle oblique line azimuth (and dependent elements)
        OR oblique line point (and dependent elements)?

        Why does there need to be two occurrences of oblique line lat/long?
    """

    pass


def orthographic(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Orthographic projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Orthographic projection.
    """

    # Create the root <orthogr> XML node for the projection.
    orthogr = xml_node("orthogr")

    # Append the longitude and latitude of the projection center to the
    # <orthogr> node.
    longpc = xml_node("longpc", params["longpc"], orthogr)
    latprjc = xml_node("latprjc", params["latprjc"], orthogr)

    # Append false easting and northing value to the <orthogr> node.
    feast = xml_node("feast", params["feast"], orthogr)
    fnorth = xml_node("fnorth", params["fnorth"], orthogr)

    return orthogr


def polar_stereographic(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Polar Stereographic projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Polar Stereographic projection.
    """

    # Create the root <polarst> XML node for the projection.
    polarst = xml_node("polarst")

    # Append xx of the projection center to the <polarst> node. ????????????????????????? what is this
    xml_node("svlong", params["svlong"], polarst)

    # Append the longitude and latitude of the projection center to the
    # <polarst> node.
    xml_node("longpc", params["longpc"], polarst)
    xml_node("latprjc", params["latprjc"], polarst)

    # Append the false easting and northing of the projection center to the
    # <polarst> node.
    xml_node("feast", params["feast"], polarst)
    xml_node("fnorth", params["fnorth"], polarst)

    return polarst


def polyconic(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Polyconic projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Polyconic projection.
    """

    # Create the root <polycon> XML node for the projection.
    polycon = xml_node("polycon")

    # Append the longitude and latitude of the projection center to the
    # <polycon> node.
    longcm = xml_node("longcm", params["longcm"], polycon)
    latprjo = xml_node("latprjo", params["latprjo"], polycon)

    # Append the false easting and northing of the projection center to the
    # <polycon> node.
    feast = xml_node("feast", params["feast"], polycon)
    fnorth = xml_node("fnorth", params["fnorth"], polycon)

    return polycon


def robinson(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Robinson projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Robinson projection.
    """

    # Create the root <robinson> XML node for the projection.
    robinson = xml_node("robinson")

    # Append the longitude of the projection center to the <robinson> node.
    longpc = xml_node("longpc", params["longpc"], robinson)

    # Append false easting and northing value to the <robinson> node.
    feast = xml_node("feast", params["feast"], robinson)
    fnorth = xml_node("fnorth", params["fnorth"], robinson)

    return robinson


def sinusoidal(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Sinusoidal projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Sinusoidal projection.
    """

    # Create the root <sinusoid> XML node for the projection.
    sinusoid = xml_node("sinusoid")

    # Append the longitude of the central meridian to the <sinusoid> node.
    longcm = xml_node("longcm", params["longcm"], sinusoid)

    # Append false easting and northing value to the <sinusoid> node.
    feast = xml_node("feast", params["feast"], sinusoid)
    fnorth = xml_node("fnorth", params["fnorth"], sinusoid)

    return sinusoid


def space_oblique_mercator(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Space Oblique Mercator projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Space Oblique Mercator projection.
    """

    # Create the root <spaceobq> XML node for the projection.
    spaceobq = xml_node("spaceobq")

    # Append the Landsat number to the <spaceobq> node.
    landsat = xml_node("landsat", params["landsat"], spaceobq)

    # Append the path number to the <spaceobq> node.
    pathnum = xml_node("pathnum", params["pathnum"], spaceobq)

    # Append false easting and northing value to the <spaceobq> node.
    feast = xml_node("feast", params["feast"], spaceobq)
    fnorth = xml_node("fnorth", params["fnorth"], spaceobq)

    return spaceobq


def stereographic(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Stereographic projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Stereographic projection.
    """

    # Create the root <stereo> XML node for the projection.
    stereo = xml_node("stereo")

    # Append the longitude and latitude of the projection center to the
    # <stereo> node.
    longpc = xml_node("longpc", params["longpc"], stereo)
    latprjc = xml_node("latprjc", params["latprjc"], stereo)

    # Append the false easting and northing value to the <stereo> node.
    feast = xml_node("feast", params["feast"], stereo)
    fnorth = xml_node("fnorth", params["fnorth"], stereo)

    return stereo


def transverse_mercator(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Transverse Mercator projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Transverse Mercator projection.

    sfctrmer = Scale Factor at Central Meridian
    longcm = Longitude of Central Meridian
    latprjo = Latitude of Projection Origin
    feast = False Easting
    fnorth - False Northing
    """

    # Create the root <transmer> XML node for the projection.
    transmer = xml_node("transmer")

    # Append the scale factor at the central meridian to the <transmer> node.
    sfctrmer = xml_node("sfctrmer", params["sfctrmer"], transmer)

    # Append the longitude and latitude of the central meridian to the
    # <transmer> node.
    longcm = xml_node("longcm", params["longcm"], transmer)
    latprjo = xml_node("latprjo", params["latprjo"], transmer)

    # Append the false easting and northing value to the <transmer> node.
    feast = xml_node("feast", params["feast"], transmer)
    fnorth = xml_node("fnorth", params["fnorth"], transmer)

    return transmer


def van_der_grinten(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the FGDC
        Van der Grinten projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params.

    Returns:
        xml_node: Lxml nodes for the FGDC Van der Grinten projection.

    longcm = Longitude of Central Meridian
    feast = False Easting
    fnorth - False Northing
    """

    # Create the root <vdgrin> XML node for the projection.
    vdgrin = xml_node("vdgrin")

    # Append the longitude of the central meridian to the <vdgrin> node.
    longcm = xml_node("longcm", params["longcm"], vdgrin)

    # Append the false easting and northing value to the <vdgrin> node.
    feast = xml_node("feast", params["feast"], vdgrin)
    fnorth = xml_node("fnorth", params["fnorth"], vdgrin)

    return vdgrin


def utm(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the
        Universal Transverse Mercator (UTM) projection.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params, including the UTM zone.

    Returns:
        xml_node: Lxml nodes for the UTM projection.
    """

    # Create the root <gridsys> XML node.
    gridsys = xml_node("gridsys")

    # Append a subnode indicating the grid system name.
    gridsysn = xml_node(
        "gridsysn", text="Universal Transverse Mercator",
        parent_node=gridsys
    )

    # Create the <utm> node under <gridsys>.
    utm_node = xml_node("utm", parent_node=gridsys)

    # Append the UTM zone to the <utm> node.
    utmzone = xml_node("utmzone", text=params["utmzone"],
                       parent_node=utm_node)

    # Create a Transverse Mercator projection node and append it to <utm>.
    transmer = transverse_mercator(params)
    utm_node.append(transmer)

    return gridsys


def spcs(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the
        State Plane Coordinate System (SPCS).

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params, including geographic coordinate system details.

    Returns:
        xml_node: Lxml nodes for the State Plane Coordinate System.
    """

    # Create the root <gridsys> XML node.
    gridsys = xml_node("gridsys")

    # Determine the correct system name based on the geographic coordinate
    # system.
    if "1983" in params["geogcs"]:
        gridsysn = xml_node(
            "gridsysn",
            text="State Plane Coordinate System 1983",
            parent_node=gridsys
        )
    else:
        gridsysn = xml_node(
            "gridsysn",
            text="State Plane Coordinate System 1927",
            parent_node=gridsys
        )

    # Create the <spcs> node under <gridsys>.
    spcs_node = xml_node("spcs", parent_node=gridsys)

    # Append the SPCS zone to the <spcs> node.
    utmzone = xml_node("spcszone", text=params["spcszone"],
                       parent_node=spcs_node)

    # Create map projection node and append it to the <spcs> node.
    mapproj_node = mapproj(params)
    spcs_node.append(mapproj_node)

    return gridsys


def arc(params):
    """
    Description:
        Returns lxml nodes that contain projection parameters for the
        ARC Coordinate System.

    Args:
        params (dict): A dictionary of geospatial parameters returned from
            get_params, including the ARC zone.

    Returns:
        xml_node: Lxml nodes for the ARC Coordinate System.
    """

    # Create the root <gridsys> XML node.
    gridsys = xml_node("gridsys")

    # Append the grid system name for ARC Coordinate System
    gridsysn = xml_node(
        "gridsysn", text="ARC Coordinate System", parent_node=gridsys
    )

    # Create the <arcsys> node under <gridsys>
    arc_node = xml_node("arcsys", parent_node=gridsys)

    # Append the ARC zone to the <arcsys> node
    arczone = xml_node("arczone", text=params["arczone"],
                       parent_node=arc_node)

    # Create a map projection node and append it to the <arcsys> node
    mapproj_node = mapproj(params)
    arc_node.append(mapproj_node)

    return gridsys


def lookup_fdgc_projname(gdal_name, mapprojn=""):
    """
    Description:
        Looks up the FGDC projection name based on the GDAL name and
        optional map projection name.

    Args:
        gdal_name (str): The name of the projection as defined in GDAL.
        mapprojn (str, optional): An optional specification of the map
            projection name.

    Returns:
        tuple: A tuple containing the FGDC projection name and its corresponding
            function. Returns (None, None) if not handled.
    """

    # Adjust the GDAL name for polar stereographic projections.
    if gdal_name == "Stereographic" and "polar" in mapprojn.lower():
        gdal_name = "Polar_Stereographic"

    # Lookup the corresponding FGDC projection.
    for k, v in PROJECTION_LOOKUP.items():
        if v["gdal_name"] == gdal_name:
            return k, v["function"]

    # Print error message if the projection is not handled.
    print("!" * 79)
    print("!" * 79)
    print("!" * 79)
    print("not handled ", gdal_name)
    print("!" * 79)
    print("!" * 79)
    print("!" * 79)

    # Return None if the projection is not found.
    return None, None  # this will blow up!


def lookup_shortname(shortname):
    for k, v in PROJECTION_LOOKUP.items():
        if v["shortname"] == shortname:
            return v
    return None


# ---------------------------------------------------------------------------
# Global lookup information for map projections
# ---------------------------------------------------------------------------
# Set up an OrderedDict named PROJECTION_LOOKUP using the collections module
# from Python. This dictionary is structured to map projection names to their
# corresponding attributes and functions.

PROJECTION_LOOKUP = collections.OrderedDict()

PROJECTION_LOOKUP["Albers Conical Equal Area"] = {
    "shortname": "albers",
    "gdal_name": "Albers_Conic_Equal_Area",
    "function": albers_conic_equal_area,
    "elements": ["stdparll", "stdparll_2", "longcm", "latprjo", "feast",
                 "fnorth"],
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
    "elements": ["stdparll", "stdparll_2", "longcm", "latprjo", "feast",
                 "fnorth"],
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
    "elements": ["stdparll", "stdparll_2", "longcm", "latprjo", "feast",
                 "fnorth"],
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
    "elements": ["stdparll", "stdparll_2", "longcm", "latprjo", "feast",
                 "fnorth"],
}

# ---------------------------------------------------------------------------
# Global lookup information for grid systems (type of map projection)
# ---------------------------------------------------------------------------
# Set up an OrderedDict named GRIDSYS_LOOKUP using the collections module
# from Python. This dictionary is structured to map projection names to their
# corresponding attributes and functions.

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

# ---------------------------------------------------------------------------
# Global lookup information for datum systems
# ---------------------------------------------------------------------------
# Set up an OrderedDict named DATUM_LOOKUP using the collections module
# from Python. This dictionary is structured to map projection names to their
# corresponding attributes and functions.
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
    Description:
        Returns the FGDC bounding element from the provided spatial file.

    Args:
        fname (str): The name of the shapefile or TIFF file for which
            the bounding box will be generated.

    Returns:
        xml_node: An lxml element representing the FGDC Bounding box.
    """

    # Retrieve the layer from the specified file.
    layer = get_layer(fname)

    # Get the geographic extent of the layer.
    extent = get_geographic_extent(layer)

    # Format the extent to adhere to the bounding element's requirements.
    extent = format_bounding(extent)

    # Create the root <bounding> XML node.
    bounding = xml_node("bounding")

    # Append bounding coordinates to the <bounding> node.
    westbc = xml_node("westbc", extent[0], bounding)
    eastbc = xml_node("eastbc", extent[1], bounding)
    northbc = xml_node("northbc", extent[2], bounding)
    southbc = xml_node("southbc", extent[3], bounding)

    return bounding


def num_sig_digits(f, min_num=4):
    """
    Description:
        Determine the number of significant digits to display for a given
        float.

    Args:
        f (float): The number used to determine the appropriate number of digits
            to return.
        min_num (int): The minimum number of digits to return.

    Returns:
        int: The number of significant digits to display.
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
    Description:
        Convert bounding coordinates to formatted strings with a
        reasonable number of decimal places.

    Args:
        extent (tuple): A tuple containing the bounding coordinates (west, east,
            north, south).

    Returns:
        list: A list of formatted strings representing the bounding
            coordinates.
    """

    # Unpack the bounding coordinates from the extent tuple.
    w, e, n, s = extent

    # Calculate the smallest dimension (width or height) to determine decimals.
    smallest_dim = min((e - w), (n - s))

    # Get the number of significant digits for formatting.
    decimals = num_sig_digits(smallest_dim)

    # Format each coordinate to the calculated number of decimal places.
    return [
        "{num:.{decimals}f}".format(num=coord, decimals=decimals) for coord in
        extent
    ]


def get_spdoinfo(fname, feature_class=None):
    """
    Description:
        Return FGDC spatial information element from the provided
        spatial file.

    Args:
        fname (str): Name of the shapefile, GeoDatabase file, or LAS file
            for which spatial information is to be generated.
        feature_class (str, optional): The name of the feature class for
            GeoDatabase files.

    Returns:
        lxml element: An object with the FGDC spatial information. Returns None
            if the format is unsupported.
    """

    # Check if the file is a shapefile.
    if fname.endswith(".shp"):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataset = driver.Open(fname)
        layer = dataset.GetLayer()
        return vector_spdoinfo(layer)

    # Check if the file is a GeoDatabase file.
    elif fname.endswith(".gdb"):
        driver = ogr.GetDriverByName("OpenFileGDB")
        gdb = driver.Open(fname, 0)
        layer = gdb.GetLayerByName(feature_class)
        return vector_spdoinfo(layer)

    # Check if the file is a LAS or LAZ file.
    elif fname.endswith(".las") or fname.endswith(".laz"):
        layer = laspy.open(fname)
        return las_spdoinfo(layer)

    # If the file extension does not match, assume it is a raster.
    else:
        data = gdal.Open(fname)
        return raster_spdoinfo(data)

    return None


def vector_spdoinfo(layer):
    """
    Description:
        Generate an FGDC Point Vector Object information element from an
        OGR layer.

    Args:
        layer (ogr.Layer): An OGR layer from which the spatial information will
            be extracted.

    Returns:
        lxml element: An XML element containing FGDC spatial information for
            the vector layer.
    """

    # Get the number of features in the layer
    feature_count = layer.GetFeatureCount()

    # Retrieve geometry type of the first feature.
    for geo in layer:
        geo_ref = geo.GetGeometryRef()
        geo_type = geo_ref.GetGeometryType()
        break

    # Create the FGDC element structure.
    spdoinfo = xml_node("spdoinfo")
    direct = xml_node("direct", text="Vector", parent_node=spdoinfo)

    ptvctinf = xml_node("ptvctinf", parent_node=spdoinfo)
    sdtsterm = xml_node("sdtsterm", parent_node=ptvctinf)

    # Determine the geometry type and create corresponding FGDC element.
    if geo_type in [3, 6, 2003, 3003, 2006, 3006]:
        sdtstype = xml_node("sdtstype", text="G-polygon",
                            parent_node=sdtsterm)
    elif geo_type in [2, 5, 2005, 3005]:
        sdtstype = xml_node("sdtstype", text="String",
                            parent_node=sdtsterm)
    elif geo_type in [1, 4, 2001, 3001, 2004, 3004]:
        sdtstype = xml_node("sdtstype", text="Entity point",
                            parent_node=sdtsterm)
    else:
        sdtstype = xml_node("sdtstype", text="Unknown",
                            parent_node=sdtsterm)

    # Add point vector count to the FGDC element.
    xml_node("ptvctcnt", text=feature_count, parent_node=sdtsterm)

    return spdoinfo


def raster_spdoinfo(data):
    """
    Description:
        Generate an FGDC Raster Object information element from a GDAL
        dataset.

    Args:
        data (gdal.dataset): A GDAL dataset from which raster information will
            be extracted.

    Returns:
        lxml element: An XML element containing FGDC spatial information for
            the raster dataset.
    """

    # Retrieve the basic raster properties.
    raster_type = "Grid Cell"  # This is the most probable answer
    cols = data.RasterXSize
    rows = data.RasterYSize
    bands = data.RasterCount

    # Create the FGDC element structure.
    spdoinfo = xml_node("spdoinfo")
    direct = xml_node("direct", text="Raster", parent_node=spdoinfo)
    rastinfo = xml_node("rastinfo", parent_node=spdoinfo)

    # Add raster properties to the FGDC element.
    rasttype = xml_node("rasttype", text=raster_type, parent_node=rastinfo)
    rowcount = xml_node("rowcount", text=rows, parent_node=rastinfo)
    colcount = xml_node("colcount", text=cols, parent_node=rastinfo)
    vrtcount = xml_node("vrtcount", text=bands, parent_node=rastinfo)

    return spdoinfo


def las_spdoinfo(layer):
    """
    Description:
        Generate an FGDC Point Vector Object information element from
        a LAS/LAZ layer.

    Args:
        layer (ogr.Layer): An OGR layer from which LAS/LAZ spatial information
            will be extracted.

    Returns:
        lxml element: An XML element containing FGDC spatial information for
            the point vector layer.
    """

    # Get the total number of points in the LAS/LAZ layer
    feature_count = layer.header.point_count

    # Create the root FGDC element
    spdoinfo = xml_node("spdoinfo")
    direct = xml_node("direct", text="Vector", parent_node=spdoinfo)

    # Create primary information elements within the FGDC structure
    ptvctinf = xml_node("ptvctinf", parent_node=spdoinfo)
    sdtsterm = xml_node("sdtsterm", parent_node=ptvctinf)

    # Specify the type of spatial data as "Point"
    sdtstype = xml_node("sdtstype", text="Point", parent_node=sdtsterm)

    # Add the point vector count to the FGDC element
    xml_node("ptvctcnt", text=feature_count, parent_node=sdtsterm)

    return spdoinfo


def band_to_df(band):
    """
    Description:
        Creates a DataFrame with one column (Value) containing the minimum
        and maximum values of the raster band.

    Args:
        band (osgeo.gdal.Band): An OSGeo raster band object from which to
            extract statistics.

    Returns:
        pandas.DataFrame: A DataFrame containing the minimum and maximum values
            of the band.
    """

    # Define the columns for the DataFrame
    cols = ["Value"]

    # Get statistics for the band (min and max values)
    stats = band.GetStatistics(True, True)

    # Prepare rows with statistics
    rows = [[stats[0]], [stats[1]]]

    # Create a DataFrame from the rows and defined columns
    df = pd.DataFrame.from_records(rows, columns=cols)

    # Ensure the 'Value' column contains floats
    df["Value"] = df["Value"].astype(float)

    return df


def get_band_count(fname):
    """
    Description:
        Retrieves the number of bands in the specified raster dataset.

    Args:
        fname (str): The file name or path to the raster dataset.

    Returns:
        int: The number of bands in the raster dataset.
    """

    # Get the raster layer from the provided file name
    raster = get_layer(fname)

    return raster.RasterCount


def rat_to_df(rat):
    """
    Description:
        Converts a raster attribute table into a pandas DataFrame.

    Args:
        rat (osgeo.gdal.RasterAttributeTable): The raster attribute table to be
            converted.

    Returns:
        pandas.DataFrame: A DataFrame representing the raster attribute table.
    """

    # Get the number of columns in the raster attribute table.
    icolcount = rat.GetColumnCount()
    cols = []

    # Retrieve column names.
    for icol in range(icolcount):
        cols.append(rat.GetNameOfCol(icol))

    # Get the number of rows in the raster attribute table.
    irowcount = rat.GetRowCount()
    rows = []

    # Retrieve values for each row.
    for irow in range(irowcount):
        vals = []
        for icol in range(icolcount):
            itype = rat.GetTypeOfCol(icol)

            # Get the value based on the column type.
            if itype == gdal.GFT_Integer:
                value = "%s" % rat.GetValueAsInt(irow, icol)
            elif itype == gdal.GFT_Real:
                value = "%.16g" % rat.GetValueAsDouble(irow, icol)
            else:
                value = "%s" % rat.GetValueAsString(irow, icol)
            vals.append(value)
        rows.append(vals)

    # Create DataFrame from the collected rows and column names.
    df = pd.DataFrame.from_records(rows, columns=cols)

    # Convert columns to appropriate types.
    for icol in range(icolcount):
        col_name = rat.GetNameOfCol(icol)
        itype = rat.GetTypeOfCol(icol)

        # Set the DataFrame column type based on the raster column type.
        if itype == gdal.GFT_Integer:
            df[col_name] = df[col_name].astype(int)
        elif itype == gdal.GFT_Real:
            df[col_name] = df[col_name].astype(float)
        else:
            df[col_name] = df[col_name].astype(str)

    return df


def get_raster_attribute_table(fname):
    """
    Description:
        Returns the raster attribute table in pandas DataFrame format.

    Args:
        fname : str
            The file name of the raster that will be used.

    Returns:
        pandas.DataFrame
            A DataFrame representing the raster attribute table.
    """

    # Get the raster layer from the specified file.
    raster = get_layer(fname)

    # Retrieve the first raster band.
    band = raster.GetRasterBand(1)

    # Get the default raster attribute table (RAT).
    rat = band.GetDefaultRAT()

    # If a RAT exists, convert it to a DataFrame.
    if rat is not None:
        df = rat_to_df(rat)

        # Check if the DataFrame has the expected column names.
        if not df.columns.equals(["Histogram"]):
            return df

    # Check for a sidecar DBF for the raster attribute table.
    vatdbf = fname + ".vat.dbf"
    if os.path.exists(vatdbf):
        # Read the DBF file using a custom read function.
        vat = data_io.read_dbf(vatdbf)

        # Ensure "OID" column exists, inserting it if necessary.
        if "OID" not in vat.columns:
            vat.insert(0, "OID", range(len(vat)))

        # Strip whitespace from string columns.
        return vat.apply(
            lambda x: x.str.strip() if x.dtype == "object" else x
        )
    else:
        # If no DBF is found, collect DataFrames from all raster bands.
        dfs = []
        for band_num in range(1, raster.RasterCount + 1):
            band = raster.GetRasterBand(band_num)
            dfs.append(band_to_df(band))

        # Concatenate DataFrames from all bands.
        df = pd.concat(dfs)

        return df


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    fname = r"wgs84.shp"
    get_spref(fname)
