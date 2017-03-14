#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a variety of spatial introspection functions.
Produces FGDC spatial elements from spatial datasets


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.

Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.

Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""

from osgeo import gdal, osr, ogr
gdal.UseExceptions()
gdal.AllRegister()

from pymdwizard.core.xml_utils import xml_node


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
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
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
        return _get_raster_extent(layer)


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

    west, north = transform_point(
        min_x, max_y, srs, srs.CloneGeogCS())
    east, south = transform_point(
        max_x, min_y, srs, srs.CloneGeogCS())

    return west, east, south, north


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
        wkt = layer.GetSpatialRef().ExportToWkt()

    return osr.SpatialReference(wkt=wkt)


def get_latlong_res(extent):
    #D. Ignizio : This function is a modified approach to calculating latitudinal and longitudinal resolution in a GCS.
    #Use in lieu of Vincenty's algorithm due to complexity/issues with incorrect results.
    #The formula calculates values against the WGS 84 spheroid.
    #The mid-point of the latitudinal extent of the dataset is used to calculate values, as they change depending on where on the globe we are considering.

    ### Find GCS bounding coordinates of DS
    min_lon, max_lon, min_lat, max_lat = extent
    #print "min_lon, min_lat, max_lon, max_lat:", min_lon, min_lat, max_lon, max_lat

    ### Find mid-latitude position while handling Hemisphere
    mid = 0
    if max_lat >= min_lat:
        mid = ((max_lat - min_lat)/2) + min_lat
    if max_lat < min_lat:
        mid = ((min_lat - max_lat)/2) + max_lat
    mid_lat = mid

    ##########################################################
    #For a WGS 84 Spheroid. See: http://en.wikipedia.org/wiki/Latitude
    #Also see: pg. 71 of the Biological Data Profile Workbook (FGDC, 2001)
    #The following points were plotted and a third-order polynomial equation was generated in MS Excel.

    # @ Degree    1 Degree Latitude (= to km)    1 Degree Longitude (= to km)
    #       0         110.574                       111.32
    #       15        110.649                       107.55
    #       30        110.852                       96.486
    #       45        111.132                       78.847
    #       60        111.412                       55.8
    #       75        111.618                       28.902
    #       90        111.694                       0
    ##########################################################

    #Length of 1 degree of Latitude in kilometers @ Latitude(y) on the globe.
    #y = -3E-06x^3 + 0.0005x^2 - 0.0013x + 110.57
    x = mid_lat
    len1DegreeLat = (-3E-06*pow(x,3)) + (0.0005*pow(x,2)) - (0.0013*x) + 110.57
    len1MinuteLat = len1DegreeLat/60
    len1SecondLat = len1MinuteLat/60

    DataScale = 24000
    DigPrecision = 0.001

    latRes = float((1/len1SecondLat) * (1/3280.84) * float(DataScale) * float(1.0/12.0) * float(DigPrecision))
    latRes = str(format(latRes, '.10f'))

    #Length of 1 degree of Longitude in kilometers @ Latitude(y) on the globe.
    #y = 7E-05x^3 - 0.0203x^2 + 0.0572x + 111.24

    len1DegreeLong = (7E-05*pow(x,3)) - (0.0203*pow(x,2)) + (0.0572*x) + 111.24
    len1MinuteLong = len1DegreeLong/60
    len1SecondLong = len1MinuteLong/60

    longRes = float((1/len1SecondLong) * (1/3280.84) * float(DataScale) * float(1.0/12) * float(DigPrecision))
    longRes = str(format(longRes, '.10f'))

    #     print "Latitude Midpoint = " + str(mid_lat)
    #     print "Latitudinal Resolution = " + latRes
    #     print "Longitudinal Resolution = " + longRes + "\n"

    return(latRes, longRes)


def get_abs_resolution(src, params):
    results = {}
    try:
        xform = src.GetGeoTransform()
        results['absc_res'] = xform[1]
        results['lat_res'] = xform[1]
        results['ord_res'] = xform[5]
        results['lon_res'] = xform[5]
    except:
        if params['pcsname'] != "[Unknown]":
            # Industry-standard digitizer precision of 0.001"
            if params['planu'] == "Feet":
                Absc_res = str(float(DataScale) * float(DigPrecision)/12.0)
                Ord_res = str(float(DataScale) * float(DigPrecision)/12.0)
            if PCS_Units == "Meter":
                Absc_res = str(float(DataScale) * (float(DigPrecision)/12.0) * 0.3048)
                Ord_res = str(float(DataScale) * (float(DigPrecision)/12.0) * 0.3048)
        if params['gcsname'] != "[Unknown]":
            gcs_extent = get_geographic_extent(src)
            lat_res, lon_res = get_latlong_res(gcs_extent)


        # The minimum difference between X (abscissa) and Y (ordinate) values in the
    #   planar data set
    # The values usually indicate the ?fuzzy tolerance? or ?clustering? setting
    #   that establishes the minimum distance at which two points will NOT be
    #   automatically converged by the data collection device (digitizer,
    #   GPS, etc.). NOTE: units of measures are provided under element Planar
    #   Distance Units
    # Raster data: Abscissa/ordinate res equals cell resolution
    # Vector data: Abscissa/ordinate res is the smallest measurable distance between
    #   coordinates
    if myDataType == "Raster":
        # Would need to loop this, but do not know how to handle metadata
        if int(str(arcpy.GetRasterProperties_management(InDS, "BANDCOUNT"))) == 1:
            # works on single band otherwise need to use different syntax
            Absc_res = str(float(desc.meanCellWidth))
            Ord_res = str(float(desc.meanCellHeight))
        else:
            # Works on multi-band as well as single band
            Absc_res = str(arcpy.GetRasterProperties_management(InDS, "CELLSIZEX"))
            Ord_res = str(arcpy.GetRasterProperties_management(InDS, "CELLSIZEX"))
        Lon_res, Lat_res = Absc_res, Ord_res
    else:

        if PCSname != "[Unknown]":
            # Industry-standard digitizer precision of 0.001"

            if PCS_Units == "Feet":
                Absc_res = str(float(DataScale) * float(DigPrecision)/12.0)
                Ord_res = str(float(DataScale) * float(DigPrecision)/12.0)
            if PCS_Units == "Meter":
                Absc_res = str(float(DataScale) * (float(DigPrecision)/12.0) * 0.3048)
                Ord_res = str(float(DataScale) * (float(DigPrecision)/12.0) * 0.3048)
        if GCSname != "[Unknown]":

            LatRes_LongRes = getLatResLongRes(GCS_ExtentList)
            Lat_res = str(LatRes_LongRes[0])
            Lon_res = str(LatRes_LongRes[1])


def get_params(layer):

    #get the spatial reference and extent
    ref = get_ref(layer)
    projected_extent = get_extent(layer)
    geographic_extent = get_geographic_extent(layer)

    params = {}

    print('\t', ref.GetAttrValue('projcs'))
    print('\t', ref.GetAttrValue('projection'))
    print('\t', ref.GetAttrValue('geogcs'))
    print('\t', ref.GetAttrValue('datum'))
    print('\t', ref.GetAttrValue('spheroid'), '\n')
            # ref.GetAttrValue('vertcs')

    # if ref.IsProjected:
    #     params['mapprojn'] =  ref.GetAttrValue('projcs')
    # if params['mapprojn'] is None:
    #     params['mapprojn'] = ''
    # else:
    # params['mapprojn'] = ''
    #
    # #GCSname
    # params['geogcs'] = ref.GetAttrValue('geogcs')


    params['latres'], params['longres'] = get_latlong_res(geographic_extent)
    params['geogunit'] = 'Decimal seconds' #we will always use Decimal Seconds'
    params['mapprojn'] = ref.GetAttrValue('projection')
    params['stdparll'] = ref.GetProjParm(osr.SRS_PP_STANDARD_PARALLEL_1)
    params['stdparll_2'] = ref.GetProjParm(osr.SRS_PP_STANDARD_PARALLEL_2)
    params['longcm'] = ref.GetProjParm(osr.SRS_PP_CENTRAL_MERIDIAN)
    params['latprjo'] = ref.GetProjParm(osr.SRS_PP_LATITUDE_OF_ORIGIN)
    params['feast'] = ref.GetProjParm(osr.SRS_PP_FALSE_EASTING)
    params['fnorth'] = ref.GetProjParm(osr.SRS_PP_FALSE_NORTHING)
    params['sfequat'] = ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR)
    params['heightpt'] = ref.GetProjParm(osr.SRS_PP_PERSPECTIVE_POINT_HEIGHT)
    params['longpc'] = ref.GetProjParm(osr.SRS_PP_LONGITUDE_OF_CENTER)
    params['latprjc'] = ref.GetProjParm(osr.SRS_PP_LATITUDE_OF_CENTER)
    params['latprjo'] = ref.GetProjParm(osr.SRS_PP_LATITUDE_OF_CENTER)
    params['sfctrlin'] = ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR)
    params['obqlazim'] = 'Unknown'
    params['azimangle'] = ref.GetProjParm(osr.SRS_PP_AZIMUTH)
    params['azimptl'] = ref.GetProjParm(osr.SRS_PP_LONGITUDE_OF_ORIGIN)
    params['obqlpt'] = 'Unknown'
    params['obqllat'] = 'Unknown'
    params['obqllong'] = 'Unknown'
    params['svlong'] = 'Unknown'
    params['sfprjorg'] = 'Unknown'
    params['landsat'] = ref.GetProjParm(osr.SRS_PP_LANDSAT_NUMBER)
    params['pathnum'] = ref.GetProjParm(osr.SRS_PP_PATH_NUMBER)
    params['sfctrmer'] = ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR)
    params['gridsysn'] = 'Unknown'
    params['utmzone'] = ref.GetUTMZone()
    params['upszone'] = 'Unknown'
    params['spcszone'] = 'Unknown'
    params['arczone'] = 'Unknown'
    params['othergrd'] = 'Unknown'
    params['localpd'] = 'Unknown'
    params['localpgi'] = 'Unknown'
    params['plance'] = 'Unknown'
    params['absres'] = 'Unknown'
    params['ordres'] = 'Unknown'
    params['distres'] = 'Unknown'
    params['bearres'] = 'Unknown'
    params['bearunit'] = 'Unknown'
    params['bearrefd'] = 'Unknown'
    params['bearrefm'] = 'Unknown'
    params['plandu'] = 'Unknown'
    params['localdes'] = 'Unknown'
    params['localgeo'] = 'Unknown'
    params['horizdn'] = ref.GetAttrValue('datum')
    params['ellips'] = ref.GetAttrValue('spheroid')
    params['localpd'] = 'Unknown'
    params['semiaxis'] = ref.GetSemiMajor()
    params['denflat'] = ref.GetInvFlattening()
    params['altdatum'] = ref.GetAttrValue('VertCSName')
    params['altres'] = 'Unknown'
    params['altunits'] = 'Unknown'
    params['altenc'] = 'Unknown'
    params['depthdn'] = 'Unknown'
    params['depthres'] = 'Unknown'
    params['depthdu'] = 'Unknown'
    params['depthem'] = 'Unknown'








    #Are all these scale factors always the same?


    params['sfctrmer'] = ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR)

    #     results['sprojorg'] = ref.GetProjParm(osr.SRS_PP_SCALE_FACTOR)


    #SPCS_Zone

    if params['mapprojn'] is not None and \
                'stateplane' in params['mapprojn'].lower():
        parts = params['mapprojn'].split('_')
        params['spcszone'] = parts[parts.index('FIPS')+1]
    #PCS_Units
    params['plandu'] = ref.GetLinearUnitsName()










    params['upzone'] = 'Unknown'
    params['arczone'] = 'Unknown'

    return params


def transform_point(x, y, from_srs, to_srs):
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
    y_round = round(y, 8)
    x_round = round(x, 8)

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
    if fname.endswith('.shp'):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataset = driver.Open(fname)
        return dataset.GetLayer()
    elif fname.endswith('.gdb'):
        driver = ogr.GetDriverByName("OpenFileGDB")
        gdb = driver.Open(fname, 0)
        return gdb.GetLayerByName(feature_class)
    else:
        #it better be a raster
        return gdal.Open(fname)

    return None


def spatial_ref(fname, feature_class=None):
    """
    Returns the ogr spatial reference object for a given filename

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
    layer = get_layer(fname)

    params = get_params(layer)

    spref = xml_node('spref')
    horizsys = xml_node('horizsys', parent_node=spref)

    if not params['mapprojn']:
        georaphic_node = geographic(params)
        horizsys.append(geographic_node)
        geodetic_node = geodetic(params)
        horizsys.append(geodetic_node)

    # if params['']


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
    latres = xml_node("latres", params['latres'], geograph)
    longres = xml_node("longres", params['longres'], geograph)
    geounit = xml_node("geogunit", params['geogunit'], geograph)
    return geograph

def albers_conic_equal_area(params):
    albers = xml_node('albers')
    stdparll = xml_node('stdparll', params['stdparll'], albers)
    if params['stdparll_2']:
        stdparll_2 = xml_node('stdparll', params['stdparll_2'], albers)

    for item in ['longcm', 'latprjo', 'feast', 'fnorth']:
        xml_node(item, params[item], albers)
    return albers


def azimuthal_equidistant(params):
    """
    returns lxml nodes that contain projection parameters for fgdc azimuthal equidistant projection

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
    lxml nodes for fgdc azimuthal equidistant projection
    """

    # This section should probably be handled in a different function?
    # planar = xml_node('planar')
    # mapproj = xml_node('mapproj', parent_node=planar)
    # mapprojn = xml_node('mapprojn', params['mapprojn'], mapproj)

    azimequi = xml_node('azimequi')
    longcm = xml_node('longcm', params['longcm'], azimequi)
    latprjo = xml_node('latprjo', params['latprjo'], azimequi)
    feast = xml_node('feast', params['feast'], azimequi)
    fnorth = xml_node('fnorth', params['fnorth'], azimequi)
    return azimequi


def equidistant_conic(params):
    """
    returns lxml nodes that contain projection parameters for fgdc equidistant conic projection

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
    lxml nodes for fgdc equidistant conic projection
    """

    equicon = xml_node('equicon')
    stdparll = xml_node('stdparll', params['stdparll'], equicon)
    if params['stdparl_2']:
        stdparll_2 = xml_node('stdparll', params['stdparll_2'], equicon)

    for item in ['longcm', 'latprjo', 'feast', 'fnorth']:
        xml_node(item, params[item], equicon)
    return equicon


def equirectangular(params):
    """
    returns lxml nodes that contain projection parameters for fgdc equirectangular projection

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
    lxml nodes for fgdc equirectangular projection
    """
    equirect = xml_node('equirect')
    stdparll = xml_node('stdparll', params['stdparll'], equirect)
    longcm = xml_node('longcm', params['longcm'], equirect)
    feast = xml_node('feast', params['feast'], equirect)
    fnorth = xml_node('fnorth', params['fnorth'], equirect)
    return equirect


def general_vertical_near_sided_perspective(params):
    """
    returns lxml nodes that contain projection parameters for fgdc General Vertical Near-sided Perspective projection

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
    gvnsp = xml_node('gvnsp')
    heightpt = xml_node('heightpt', params['heightpt'], gvnsp)
    longpc = xml_node('longpc', params['longpc'], gvnsp)
    latprjc = xml_node('latprjc', params['latprjc'], gvnsp)
    feast = xml_node('feast', params['feast'], gvnsp)
    fnorth = xml_node('fnorth', params['fnorth'], gvnsp)
    return gvnsp
























PROJECTION_LOOKUP = {'Albers Conical Equal Area':{'shortname': 'albers',
                                  'elements': ['stdparll', 'stdparl_2',
                                               'longcm',
                                               'latprjo', 'feast', 'fnorth']},
                     'Azimuthal Equidistant':{'shortname':'azimequi',
                                    'elements': ['longcm', 'latprjo', 'feast', 'fnorth']},
                     'Equidistant Conic':{'shortname':'equicon',
                                    'elements': ['longcm', 'latprjo', 'feast', 'fnorth']},
                     'Equirectangular':{'shortname':'equirect',
                                    'elements': ['stdparll', 'longcm', 'feast', 'fnorth']},
                     'General Vertical Near-sided Perspective':{'shortname':'gvnsp',
                                    'elements': ['heightpt', 'longpc', 'latprjc', 'feast', 'fnorth']}
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

    bounding = xml_node('bounding')
    westbc = xml_node('westbc', extent[0], bounding)
    eastbc = xml_node('eastbc', extent[1], bounding)
    northbc = xml_node('northbc', extent[3], bounding)
    southbc = xml_node('southbc', extent[2], bounding)

    return bounding

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
    if fname.endswith('.shp'):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataset = driver.Open(fname)
        layer = dataset.GetLayer()
        return vector_spdoinfo(layer)
    elif fname.endswith('.gdb'):
        driver = ogr.GetDriverByName("OpenFileGDB")
        gdb = driver.Open(fname, 0)
        layer = gdb.GetLayerByName(feature_class)
        return vector_spdoinfo(layer)
    else:
        #it better be a raster
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
    #introspect our layer to get the info we need
    feature_count = layer.GetFeatureCount()
    for geo in data:
        geo_ref = geo.GetGeometryRef()
        geo_type = geo_ref.GetGeometryType()
        break

    #create the FGDC element
    spdoinfo = xml_node('spdoinfo')
    direct = xml_node('direct', text='Vector', parent_node=spdoinfo)

    ptvctinf = xml_node('ptvctinf', parent_node=spdoinfo)
    sdtsterm = xml_node('sdtsterm', parent_node=ptvctinf)

    if geo_type == 3:
        sdtstype = xml_node('sdtstype', text='G-polygon', parent_node=sdtsterm)
    elif geo_type == 2:
        sdtstype = xml_node('sdtstype', text='String', parent_node=sdtsterm)
    elif geo_type == 1:
        sdtstype = xml_node('sdtstype', text='Entity point',
                            parent_node=sdtsterm)

    xml_node('ptvctcnt', text = feature_count, parent_node=sdtsterm)
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
    #introspect our data to get the info we need
    raster_type = "Grid Cell" # This is the most probable answer
    cols = data.RasterXSize
    rows = data.RasterYSize
    bands = data.RasterCount

    #create the FGDC element
    spdoinfo = xml_node('spdoinfo')
    direct = xml_node('direct', text='Raster', parent_node=spdoinfo)
    rastinfo = xml_node('rastinfo', parent_node=spdoinfo)

    rasttype = xml_node('rasttype', text=raster_type, parent_node=rastinfo)
    rowcount = xml_node('rowcount', text=rows, parent_node=rastinfo)
    colcount = xml_node('colcount', text=cols, parent_node=rastinfo)
    vrtcount = xml_node('vrtcount', text=bands, parent_node=rastinfo)

    return spdoinfo