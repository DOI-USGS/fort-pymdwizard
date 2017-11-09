"""
This collection of tools was originally created by Michael O'Donnell at the USGS Fort Collins Science Center (FORT).


"""
import os, sys, subprocess, time, stat
import arcpy 
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
import math

GeogCoordUnits = ["Decimal degrees", "Decimal minutes", "Decimal seconds",
    "Degrees and decimal minutes", "Degrees, minutes, and decimal seconds",
    "Radians", "Grads"]

### Metadata Element Tabs
#ElemTab_1 = "\n\t"
#ElemTab_2 = "\n\t\t"
#ElemTab_3 = "\n\t\t\t"
#ElemTab_4 = "\n\t\t\t\t"
#ElemTab_5 = "\n\t\t\t\t\t"
#ElemTab_6 = "\n\t\t\t\t\t\t"
#ElemTab_7 = "\n\t\t\t\t\t\t\t"
#ElemTab_8 = "\n\t\t\t\t\t\t\t\t"
#ElemTab_9 = "\n\t\t\t\t\t\t\t\t\t"

Vertical_CS_Switch = ""
DataScale = 24000
DigPrecision = 0.001

ElemTab_1 = ""
ElemTab_2 = ""
ElemTab_3 = ""
ElemTab_4 = ""
ElemTab_5 = ""
ElemTab_6 = ""
ElemTab_7 = ""
ElemTab_8 = ""
ElemTab_9 = ""

def getLatResLongRes(GCS_ExtentList):
    #D. Ignizio : This function is a modified approach to calculating latitudinal and longitudinal resolution in a GCS.
    #Use in lieu of Vincenty's algorithm due to complexity/issues with incorrect results.
    #The formula calculates values against the WGS 84 spheroid.
    #The mid-point of the latitudinal extent of the dataset is used to calculate values, as they change depending on where on the globe we are considering.

    ### Find GCS bounding coordinates of DS
    # GCS_ExtentList = [extent.XMin, extent.YMin, extent.XMax, extent.YMax]
    min_lon = GCS_ExtentList[0]
    min_lat = GCS_ExtentList[1]
    max_lon = GCS_ExtentList[2]
    max_lat = GCS_ExtentList[3]
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
    
    latRes = float((1/len1SecondLat) * (1/3280.84) * float(DataScale) * float(1.0/12.0) * float(DigPrecision))
    latRes = str(format(latRes, '.10f'))
    
    #Length of 1 degree of Longitude in kilometers @ Latitude(y) on the globe.
    #y = 7E-05x^3 - 0.0203x^2 + 0.0572x + 111.24

    len1DegreeLong = (7E-05*pow(x,3)) - (0.0203*pow(x,2)) + (0.0572*x) + 111.24
    len1MinuteLong = len1DegreeLong/60
    len1SecondLong = len1MinuteLong/60
    
    longRes = float((1/len1SecondLong) * (1/3280.84) * float(DataScale) * float(1.0/12) * float(DigPrecision))
    longRes = str(format(longRes, '.10f'))
    
    print "Latitude Midpoint = " + str(mid_lat)
    print "Latitudinal Resolution = " + latRes
    print "Longitudinal Resolution = " + longRes + "\n"
    
    return(latRes, longRes)

#====================================================================
# Spatial Reference for updating XML metadata templates
#====================================================================
### Spatial Reference Open
    
def Open_SpatialRef():
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_1 + "<spref>")
    FileOutW.close()
    del FileOutW

def Close_SpatialRef():
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_1 + "</spref>")
    FileOutW.close()
    del FileOutW

### Horizontal coordinate system
def Open_Horizontal():
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_2 + "<horizsys>")
    FileOutW.close()
    del FileOutW

def Close_Horizontal():
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_2 + "</horizsys>")
    FileOutW.close()
    del FileOutW


def XML_SpatialReference(SR_List, myDataType):
    #DI: myDataType added as passed input parameter.


    ### ----------------------------------------------------------------------------
    ### Create compound element for spatial reference
    Open_SpatialRef()
    Open_Horizontal()

    ### ------------------------------------- Horizontal Coordinate System
    # Geographic coordinate system--"GCSname" is defined for map projections so
    #   check whether PCSname is unknown
    if SR_List["PCSname"] == "[Unknown]":
        Geographic(SR_List)

        # Add geodetic Model now; this is used if using an ellipsoid or spheroid
        Geodetic(SR_List)

    ### ------------------------------------- Include this in addition to horizontal when applicable
    # Vertical coordinate system
    if Vertical_CS_Switch == "Present" or SR_List["VCSname"] != "[Unknown]":
        Vertical_CS(SR_List)

    # Projected map projection and Grid map projection
    elif SR_List["PCSname"] != "[Unknown]":
        if SR_List["UTM_Zone"] == "[Unknown]" and SR_List["SPCS_Zone"] == "[Unknown]" and \
                SR_List["UPS_Zone"] == "[Unknown]" and SR_List["Arc_Zone"] == "[Unknown]":
            
            # Map Projection
            #ProjName = SR_List["PrjName"].lower().replace("_", " ")
            ProjName = SR_List["ProjType"].lower().replace("_", " ")
            
            if "albers" in ProjName:
                Albers_Conical_Equal_Area(SR_List)
            elif "azimuthal" in ProjName and "equidistant" in ProjName:
                Azimuthal_Equidistant(SR_List)
            elif "equidistant" in ProjName and "conic" in ProjName:
                Equidistant_Conic(SR_List)
            elif "equirectangular" in ProjName:
                Equirectangular(SR_List)
            elif "general" in ProjName and "vertical" in ProjName and "near" in ProjName and "perspective" in ProjName:
                General_Vertical_Near_sided_Perspective(SR_List)
            elif "gnomonic" in ProjName:
                Gnomonic(SR_List)
            elif "lambert" in ProjName and "azimuthal" in ProjName:
                Lambert_Azimuthal_Equal_Area(SR_List)
            elif "lambert" in ProjName and "conformal" in ProjName and "conic" in ProjName:
                Lambert_Conformal_Conic(SR_List)
            elif "modified" in ProjName and "stereographic" in ProjName and "alaska" in ProjName:
                Modified_Stereographic_for_Alaska()
            elif "miller" in ProjName and "cylindrical" in ProjName:
                Miller_Cylindrical(SR_List)
            
            elif "space" in ProjName and "oblique" in ProjName and "mercator" in ProjName and "landsat" in ProjName:
                Space_Oblique_Mercator_Landsat(SR_List)            
            elif "transverse" in ProjName and "mercator" in ProjName:
                Transverse_Mercator(SR_List)           
            elif "oblique" in ProjName and "mercator" in ProjName:
                Oblique_Mercator(SR_List)                        
            elif "mercator" in ProjName:
                Mercator(SR_List)


            elif "polar" in ProjName and "stereographic" in ProjName:
                Polar_Stereographic(SR_List)
            elif "stereographic" in ProjName:
                Stereographic(SR_List)            
            
            
            elif "orthographic" in ProjName:    
                Orthographic(SR_List)
            elif "polyconic" in ProjName:
                Polyconic(SR_List)
            elif "robinson" in ProjName:
                Robinson(SR_List)
            elif "sinusoidal" in ProjName:
                Sinusoidal(SR_List)
            elif "van" and "der" and "grinten" in ProjName:
                van_der_Grinten(SR_List)
            else:
                Other_MapProjections(SR_List)

        else:
            if SR_List["UTM_Zone"] != "[Unknown]":
                Universal_Transverse_Mercator(SR_List)
            elif SR_List["SPCS_Zone"] != "[Unknown]":
                State_Plane_Coordinate_System(SR_List)
            elif SR_List["UPS_Zone"] != "[Unknown]":
                Universal_Polar_Stereographic(SR_List)
            elif SR_List["Arc_Zone"] != "[Unknown]":
                ARC_Coordinate_System(SR_List)
            else:
                # This will not work because do not have a mechanism to determine
                #   whether using a grid or not (instead it will go into Other_MapProjections())
                Other_Grid_System(SR_List)

        # Planar coordinate Information
        Planar_CoordInfo(myDataType, SR_List)

        # Add geodetic Model now; this is used if using an ellipsoid or spheroid
        Geodetic(SR_List)

    ### ------------------------------------- Local -- not including
    else:
        pass


    ### Close horizon compound element for spatial reference
    Close_Horizontal()

    ### ------------------------------------- Include this in addition to horizontal when applicable
    # Vertical coordinate system
    if Vertical_CS_Switch == "Present":
        Vertical_CS(SR_List)


    ### Close compound element for spatial reference
    Close_SpatialRef()
    
def Geographic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<geograph>")
    FileOutW.write(ElemTab_4 + "<latres>" + str(SR_List["Lat_res"]) + "</latres>")
    FileOutW.write(ElemTab_4 + "<longres>" + str(SR_List["Lon_res"]) + "</longres>")
    #FileOutW.write(ElemTab_4 + "<geogunit>" + SR_List["GCS_Units"] + "</geogunit>")
    FileOutW.write(ElemTab_4 + "<geogunit>Decimal seconds</geogunit>")#Calculation will always return value in Decimal Seconds
    FileOutW.write(ElemTab_3 + "</geograph>")
    FileOutW.close()
    del FileOutW

def Get_SpatialRef(SR_InDS, myDataType, myFeatType, GCS_ExtentList, desc, InDS):
    #DI: desc, InDS added as input parameters

    ### Default units for GCS and PCS
    PCSname = "[Unknown]"
    PrjName = "[Unknown]"
    ProjType = "[Unknown]" #DI Added
    GCSname = "[Unknown]"
    PCS_Units = "[Unknown]"
    GCS_Units = "[Unknown]"
    Azimuth = "[Unknown]"
    latOf1stPt = "[Unknown]"
    latOf2ndPt = "[Unknown]"
    longOf1stPt = "[Unknown]"
    longOf2ndPt = "[Unknown]"
    DatumName = "[Unknown]"
    SpheroidName = "[Unknown]"
    PrimeMeridName = "[Unknown]"
    PrimeMeridDeg = "[Unknown]"
    SP1 = "[Unknown]"
    SP2 = "[Unknown]"
    LongCM = "[Unknown]"
    ProjCM = "[Unknown]"
    LatPrjOrigin = "[Unknown]"
    SF = "[Unknown]"
    FE = "[Unknown]"
    FN = "[Unknown]"
    UTM_Zone = "[Unknown]"
    SPCS_Zone = "[Unknown]"
    UPS_Zone = "[Unknown]"
    Arc_Zone = "[Unknown]"
    a = "[Unknown]"
    f = "[Unknown]"
    Absc_res = "[Unknown]"
    Ord_res = "[Unknown]"
    Lat_res = "[Unknown]"
    Lon_res = "[Unknown]"
    Height = "[Unknown]"
    VCSname = "[Unknown]"
    VCSdatum = "[Unknown]"
    VCS_Units = "[Unknown]"
    VCS_res = "[Unknown]"


    # http://www.geoapi.org/2.0/javadoc/org/opengis/referencing/doc-files/WKT.html
    # -------------------------------------------------------------------------
    # VERTCS['National_Geodetic_Vertical_Datum_1929',
    #   VDATUM['NGVD_1929'],
    #   PARAMETER['Vertical_Shift',0.0],
    #   PARAMETER['Direction',1.0],
    #   UNIT['Meter',1.0]
    # ]
    # -------------------------------------------------------------------------
    # "PROJCS['Albers_Conical_Equal_Area',
    #   GEOGCS['GCS_WGS_1984',
    #       DATUM['D_WGS_1984', SPHEROID['WGS_1984',6378137.0,298.257223563]]
    #       PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]
    #   ]
    #   PROJECTION['Albers'],
    #   PARAMETER['False_Easting',0.0],
    #   PARAMETER['False_Northing',0.0],
    #   PARAMETER['central_meridian',-96.0],
    #   PARAMETER['Standard_Parallel_1',29.5],
    #   PARAMETER['Standard_Parallel_2',45.5],
    #   PARAMETER['latitude_of_origin',23.0],
    #   UNIT['Meter',1.0]
    # ]
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Not sure what these precisions are for yet
    # ;-16901100 -6972200 266467840.990852;
    # -100000 10000;
    # -100000 10000;
    # 0.001;
    # 0.001;
    # 0.001;
    # IsHighPrecision"

    ### Break the string into pieces so each item will be something we can work with
    SR_string = SR_InDS.exportToString()
    # tmp_CSV = re.split('\[*\]', CRS)
    try: CRS = str(SR_string.split(";")[0])
    except: CRS = SR_string

    ### Determine if data uses map projection or geographic coord sys
    if str(SR_InDS.PCSname) != "":
        PCSname = str(SR_InDS.PCSname)
    if str(SR_InDS.GCSname) != "":
        GCSname = str(SR_InDS.GCSname)
    if str(SR_InDS.GCSname) != "":
        PrjName = "[Unknown]"
    else:
        PrjName = str(SR_InDS.name)
    if "VERTCS[" in SR_string:
        try:
            VCS = CRS.split(",VERTCS[")[1]
            VCSname = VCS.split(",")[0].strip("'")
        except:
            VCSname = "[Unknown]"
    else:
        VCSname = "[Unknown]"


    ### D. Ignizio (Added. Populate new 'ProjType' variable to help with some projections)
    try:
        ProjType = ProjType = CRS.split(",PROJECTION[")[1].split("]")[0].strip("'")
    except:
        pass

    
    
    ### Map Projection information ---------------------------------------------
    if PCSname != "[Unknown]":
        ### Alter projection name for certain map projections
        if "van_der_grinten" in PrjName.lower():
            PrjName = "van der Grinten"
        if "Vertical_Near_Side_Perspective" == PrjName:
            PrjName = "General Vertical Near-sided Perspective"
        PrjName = PrjName.replace("_", " ")
        if PrjName == "":
            PrjName = "[Unknown]"

        try: PROJCS = CRS.split(",PROJECTION[")[0]
        except: PROJCS = "[Unknown]"
        try: PROJCS2 = PROJCS.split(",GEOGCS[")[0]
        except: PROJCS2 = "[Unknown]"
        try:
            GEOGCS = PROJCS.split(",GEOGCS[")[1]
        except: GEOGCS = "[Unknown]"
        try:
            PROJECTION = CRS.split(",PROJECTION")[1]
            PROJECTION2 = PROJECTION.split("],")
        except: PROJECTION2 = "[Unknown]"

        try:
            Azimuth = str(float(SR_InDS.azimuth))
            if float(Azimuth) < 0.00000001e-25: Azimuth = "[Unknown]"
        except: pass
        #
        try:
            latOf1stPt = str(float(SR_InDS.latitudeOf1st))
            if float(latOf1stPt) < 0.00000001e-25: latOf1stPt = "[Unknown]"
        except: pass
        #
        try:
            latOf2ndPt = str(float(SR_InDS.latitudeOf2nd))
            if float(latOf2ndPt) < 0.00000001e-25: latOf2ndPt = "[Unknown]"
        except: pass
        #
        try:
            longOf1stPt = str(float(SR_InDS.longitudeOf1st))
            if float(longOf1stPt) < 0.00000001e-25: longOf1stPt = "[Unknown]"
        except: pass
        #
        try:
            longOf2ndPt = str(float(SR_InDS.longitudeOf2nd))
            if float(longOf2ndPt) < 0.00000001e-25: longOf2ndPt = "[Unknown]"
        except: pass
        #
        try:
            LongCM = str(float(SR_InDS.centralMeridian))
        except: pass
        #
        try: SF = str(float(SR_InDS.scaleFactor))
        except: pass
        #
        try:
            SP1 = str(float(SR_InDS.standardParallel1))
            SP2 = str(float(SR_InDS.standardParallel2))
        except: pass
        #
        try: FE = str(float(SR_InDS.falseEasting))
        except: pass
        try: FN = str(float(SR_InDS.falseNorthing))
        except: pass
        #
        try: PCS_Units = str(SR_InDS.linearUnitName)
        except:
            if PCS_Units == "": PCS_Units = "[Unknown]"
        #
        try:
            ProjCM = str(float(SR_InDS.longitudeOfOrigin))
            if float(ProjCM) < 0.00000001e-25: ProjCM = "[Unknown]"
        except: pass
        #
        try:
            PROJECTION_tmp = PROJECTION.lower() # Discrepancies how ESRI writes this
            tmp = PROJECTION_tmp.split("PARAMETER['latitude_of_origin".lower())[1]
            tmp2 = tmp.split("],")[0]
            LatPrjOrigin = str(float(tmp2.strip("\',")))
        except: pass

        ### Extract Geographic info from SRS string for map projections
        ###   ESRI objects will not work when map projection exists, and
        ###   therefore this method is required to populate metadata
        try:
            GCSname = GEOGCS.split(",")[0].strip("'")
        except: pass
        #
        try:
            tmp = GEOGCS.split("DATUM[")[1]
            DatumName = tmp.split(",")[0].strip("'")
        except: pass
        #
        try:
            tmp = GEOGCS.split("SPHEROID[")[1]
            SpheroidName = tmp.split(",")[0].strip("'")
        except: pass
        #
        try:
            tmp = GEOGCS.split("PRIMEM[")[1]
            PrimeMeridName = tmp.split(",")[0].strip("'")
        except: pass
        #
        try:
            # ??????????????????????????????????
            LongPM = "[Unknown]"
        except: pass
        #
        try:
            tmp = GEOGCS.split("UNIT[")[1]
            tmp2 = tmp.split(",")[0]
            GCS_Units = tmp2.strip("'")
        except: pass
        #
        try:
            tmp = GEOGCS.split("PRIMEM[")[1]
            tmp2 = tmp.split("],")[0]
            PrimeMeridDeg = str(float(tmp2.split(",")[1]))
        except: pass

        ### Get zone when applicable -----------------------------------------------
        # Zones--Caution: if a custom projection is used, but name was not changed or
        #   if name changed and does not follow the ESRI protocol, this will not work.
        # We could derive from CM (UTM) and lat (UPS), but not sure how to derive for
        #   ARC or SPCS
        # For now, we will use this method since FORT does not generally use these
        #   map projections
        Name = str(SR_InDS.name)
        Name2 = Name.split("_")
        len_Name = len(Name2)
        if "UTM" in Name2:
            try:
                UTM_Zone = Name2[len_Name-1]
                UTM_Zone = UTM_Zone.replace("N", "")
                UTM_Zone = UTM_Zone.replace("S", "")
            except:pass
        
        if "StatePlane" in Name2:
            #Handle State Plane Coordinate System Based for FGDC-CSDGM formatting
            '''
            Example:
            PROJCS['NAD_1983_StatePlane_Alaska_2_FIPS_5002',
            GEOGCS['GCS_North_American_1983',
            DATUM['D_North_American_1983',
            SPHEROID['GRS_1980',6378137.0,298.257222101]],
            PRIMEM['Greenwich',0.0],
            UNIT['Degree',0.0174532925199433]],
            PROJECTION['Transverse_Mercator'],
            PARAMETER['False_Easting',500000.0],
            PARAMETER['False_Northing',0.0],
            PARAMETER['Central_Meridian',-142.0],
            PARAMETER['Scale_Factor',0.9999],
            PARAMETER['Latitude_Of_Origin',54.0],
            UNIT['Meter',1.0]];
            -5122600 -15986400 450310428.589905;
            -100000 10000;
            -100000 10000;
            0.001;
            0.001;
            0.001;
            IsHighPrecision
            '''
            
            ########################################
            #Get the State Plane Coordinate System Zone number. 
            try:
                termCt = 0
                while isinstance(SPCS_Zone, int) == False:
                    termCt +=1
                    try:
                        SPCS_Zone = int(Name2[len_Name-termCt])#Count back from the end.
                    except:
                        SPCS_Zone = Name2[len_Name-termCt]
                    
                    #if len()                        
            except:
                pass
            SPCS_Zone = str(SPCS_Zone)
            
            #Must be a 4-digit number. The shortest is 3 digits, so we can check and prepend a '0'.
            if len(SPCS_Zone)<4:
                SPCS_Zone = "0" + SPCS_Zone                       
            ########################################
        
        
        if "UPS" in Name2:
            try:
                # "A", "B", "Y", "Z" -- How do I get this info
                UPS_Zone = Name2[len_Name-1] # North or south
            except:pass
        if "ARC" in Name2:
            try:
                Arc_Zone = Name2[len_Name-1]
            except:pass


    ### Geographic coordinate system information -------------------------------
    if GCSname != "[Unknown]":
        try:
            if str(SR_InDS.GCSname) != "": GCSname = str(SR_InDS.GCSname)
        except: pass
        #
        try:
            if str(SR_InDS.datumName) != "": DatumName = str(SR_InDS.datumName)
        except: pass
        #
        try:
            if str(SR_InDS.spheroidName) != "": SpheroidName = str(SR_InDS.spheroidName)
        except: pass
        #
        try:
            if str(SR_InDS.primeMeridianName) != "": PrimeMeridName = str(SR_InDS.primeMeridianName)
        except: pass
        #
        try:
            LongPM = str(float(SR_InDS.longitude))
            if float(LongPM) < 0.00000001e-25: LongPM = "[Unknown]"
        except: pass
        #
        try:
            GEOGCS = CRS.split("GEOGCS[")[1]
        except: GEOGCS = "[Unknown]"
        #
        try:
            tmp = GEOGCS.split("UNIT[")[1]
            tmp2 = tmp.split(",")[0]
            GCS_Units = tmp2.strip("\'")
        except: pass
        #
        try:
            tmp = GEOGCS.split("PRIMEM[")[1]
            tmp2 = tmp.split("],")[0]
            PrimeMeridDeg = str(float(tmp2.split(",")[1]))
        except: pass


    ### Vertical coordinate system information ---------------------------------
    if VCSname != "[Unknown]":
        try:
            tmp = str(VCS.split("VDATUM[")[1])
            VCSdatum = tmp.split("],")[0].strip("'")
        except: pass
        #
        try:
            tmp = str(VCS.split("UNIT[")[1])
            VCS_Units = tmp.split(",")[0].strip("'")
        except: pass
        #
        try:
            # ?????????????????????????
            tmp = str(VCS.split("PARAMETER['Direction")[1])
            tmp2 = tmp.split("],")[0].strip("'")
            VCS_res = str(float(tmp2.strip(",")))
        except: pass
        #
        try:
            tmp = str(VCS.split("PARAMETER['Vertical_Shift")[1])
            tmp2 = tmp.split("],")[0].strip("'")
            Height = str(float(tmp2.strip(",")))
        except: pass


    ### Flattening ratio -------------------------------------------------------
    # Make sure these units are always meters, otherwise convert--ESRI will
    #   always use meters I believe so do not need to worry about this.
    # This will work for both map projection and GCS because we extract 'GEOGCS'
    #   differently using code.
    # a = semimajor axis
    # b = semiminor axis
    # Flattening ratio: f = (a-b)/a
    #try: f = float(SR_InDS.flattening)
    #except: pass
    try:
        tmp = GEOGCS.split("SPHEROID[")[1]
        tmp2 = tmp.split("]],")[0]
        tmp3 = tmp2.split(",")
        a = float(tmp3[1]) # We still need this
        #b = float(tmp3[2]) # This is not the minor axis and ESRI gives us the 1/f value here
        f = float(tmp3[2]) # FGDC requires 1/f, which is the value that ESRI uses in their projection file
        if f > 0.0:
            f2 = float(1.0 / f) # actual flattening ratio (not what ESRI uses in their projection file)
            #f = float((a - b) / a)                                                            
        else:
            f2 = 0.0

        a = str(a)
        f = str(f)
        f2 = str(f2)
    except:
        f2 = "0.0"
        f = "0.0"
        a = "0.0"


    ### Coordinate resolution for all coord sys and data types
    # Planar coordinate info
    #   Coord encoding method
    #   Abscissa res
    #   Ordinate res
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
            
    ### Return dictionary object for populating metadata
    SR_List = \
        {"PCSname": PCSname,
        "PrjName": PrjName,
        "ProjType": ProjType, #Added.
        "GCSname": GCSname,
        "GCS_Units": GCS_Units,
        "PCS_Units": PCS_Units,
        "Azimuth": Azimuth,
        "latOf1stPt": latOf1stPt,
        "latOf2ndPt": latOf2ndPt,
        "longOf1stPt": longOf1stPt,
        "longOf2ndPt": longOf2ndPt,
        "DatumName": DatumName,
        "SpheroidName": SpheroidName,
        "SP1": SP1,
        "SP2": SP2,
        "LongCM": LongCM,
        "ProjCM": ProjCM,
        "LatPrjOrigin": LatPrjOrigin,
        "SF": SF,
        "FE": FE,
        "FN": FN,
        "UTM_Zone": UTM_Zone,
        "SPCS_Zone": SPCS_Zone,
        "UPS_Zone": UPS_Zone,
        "Arc_Zone": Arc_Zone,
        "a": a,
        "f": f,
        "Absc_res": Absc_res,
        "Ord_res": Ord_res,
        "Lat_res": Lat_res,
        "Lon_res": Lon_res,
        "Height": Height,
        "VCSname": VCSname,
        "VCSdatum": VCSdatum,
        "VCS_Units": VCS_Units,
        "VCS_res": VCS_res}

    #print str(SR_List)
    return SR_List


#====================================================================
# Planar Map Projections for updating XML metadata templates
#====================================================================
def Albers_Conical_Equal_Area(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    #FileOutW.write(ElemTab_5 + "<mapprojn>Albers Conical Equal Area (" + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<albers>")
    # Std Paral 1
    # Std Paral 2 (if exists)
    # Long of central Meridian
    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")
    if SR_List["SP2"] != "[Unknown]":
        FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP2"] + "</stdparll>")
    else: pass
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</albers>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


def Azimuthal_Equidistant(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<azimequi>")
    # Long of central Meridian
    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</azimequi>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


def Equidistant_Conic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<equicon>")
    # Std Paral 1
    # Std Paral 2 (if exists)
    # Long of central Meridian
    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")
    if SR_List["SP2"] != "[Unknown]":
        FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP2"] + "</stdparll>")
    else: pass
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</equicon>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


def Equirectangular(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<equirect>")
    # Std Paral 1
    # Long of central Meridian
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</equirect>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


def General_Vertical_Near_sided_Perspective(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<gvnsp>")
    # Height of perspective point above surface
    # Longitude of Projection Center
    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<heightpt>" + SR_List["Height"] + "</heightpt>")
    FileOutW.write(ElemTab_6 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</gvnsp>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


def Gnomonic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<gnomonic>")
    # Long of Projection Center
    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</gnomonic>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


def Lambert_Azimuthal_Equal_Area(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<lamberta>")
    # Long of Projection Center
    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</lamberta>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


def Lambert_Conformal_Conic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<lambertc>")
    # Std paral 1
    # Std paral 2 (if exists)
    # Long of Central Meridian
    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")
    if SR_List["SP2"] != "[Unknown]":
        FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP2"] + "</stdparll>")
    else: pass
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</lambertc>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


def Mercator(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<mercator>")
    # Std paral 1 (or scale factor at equator)
    # Long of Central Meridian
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</mercator>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Modified_Stereographic_for_Alaska(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<modsak>")
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</modsak>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Miller_Cylindrical(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<miller>")
    FileOutW.write(ElemTab_5 + "<mapprojp>")
    # Long of Central Meridian
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</miller>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Oblique_Mercator(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<obqmerc>")
    # Scale Factor at Center Line
    FileOutW.write(ElemTab_6 + "<sfctrlin>" + SR_List["SF"] + "</sfctrlin>")

    # --
    # Oblique Line Azimuth
    #   Azimuthal Angle
    #   Azimuth Measure Point Longitude
    FileOutW.write(ElemTab_6 + "<obqlazim>")
    FileOutW.write(ElemTab_7 + "<azimangl>[Unknown]</azimangl>") #????????????????????????????????????????????????
    FileOutW.write(ElemTab_7 + "<azimptl>[Unknown]</azimptl>") #????????????????????????????????????????????????
    FileOutW.write(ElemTab_6 + "</obqlazim>")
    # OR
    # Oblique Line Point
    #   (two occurrences of both)??
    #   Oblique Line Latitude
    #   Oblique Line Longitude
    FileOutW.write(ElemTab_6 + "<obqlpt>")
    FileOutW.write(ElemTab_7 + "<obqllat>[Unknown]</obqllat>") #????????????????????????????????????????????????
    FileOutW.write(ElemTab_7 + "<obqllat>[Unknown]</obqllat>") #????????????????????????????????????????????????
    FileOutW.write(ElemTab_7 + "<obqllong>[Unknown]</obqllong>") #????????????????????????????????????????????????
    FileOutW.write(ElemTab_7 + "<obqllong>[Unknown]</obqllong>") #????????????????????????????????????????????????
    FileOutW.write(ElemTab_6 + "</obqlpt>")
    # ---

    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")

    FileOutW.write(ElemTab_5 + "</obqmerc>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Orthographic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<orthogr>")
    # Longitude of Projection Center
    # Latitude of Projection Center
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</orthogr>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Polar_Stereographic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<polarst>")
    # Straight-Vertical Longitude from Pole
    FileOutW.write(ElemTab_6 + "<svlong>[Unknown]</svlong>") #????????????????????????????????????????????????
    # ---
    # Standard Parallel
    FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")

    # OR
    # Scale Factor at Projection Origin
    FileOutW.write(ElemTab_6 + "<sfprjorg>" + SR_List["SF"] + "</sfprjorg>")
    # ---
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")

    FileOutW.write(ElemTab_5 + "</polarst>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Polyconic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<polycon>")
    # Longitude of Central Meridian
    # Latitude of Projection Origin
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</polycon>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Robinson(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<robinson>")
    # Longitude of Projection Center
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</robinson>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Sinusoidal(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<sinusoid>")
    # Longitude of Central Meridian
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</sinusoid>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Space_Oblique_Mercator_Landsat(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<spaceobq>")
    # Landsat Number
    # Path Number
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<landsat>[Landsat Platform Number]</landsat>")
    FileOutW.write(ElemTab_6 + "<pathnum>[Landsat Path Number]</pathnum>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</spaceobq>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Stereographic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<stereo>")
    # Longitude of Projection Center
    # Latitude of Projection Center
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
    FileOutW.write(ElemTab_6 + "<latprjc>" + SR_List["LatPrjOrigin"] + "</latprjc>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</stereo>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Transverse_Mercator(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<transmer>")
    # Scale Factor at Central Meridian
    # Longitude of Projection Center
    # Latitude of Projection Center
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<sfctrmer>" + SR_List["SF"] + "</sfctrmer>")
    FileOutW.write(ElemTab_6 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
    FileOutW.write(ElemTab_6 + "<latprjc>" + SR_List["LatPrjOrigin"] + "</latprjc>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</transmer>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def van_der_Grinten(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<vdgrin>")
    # Longitude of Projection Center
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_5 + "</vdgrin>")
    FileOutW.write(ElemTab_4 + "</mapproj>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Other_MapProjections(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<mapproj>")
    FileOutW.write(ElemTab_5 + "<mapprojn>" + SR_List["PrjName"] + " (ESRI Full Name: " + SR_List["PCSname"] + ")</mapprojn>")
    FileOutW.write(ElemTab_5 + "<mapprojp>[Need to define name, parameter and reference]</mapprojp>")
    FileOutW.write(ElemTab_4 + "</mapproj>") #DI: Added.
    # Enumerate parameters and include if defined (in correct order) ?????????? Not complete
    FileOutW.close()
    del FileOutW

def Universal_Transverse_Mercator(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<gridsys>")
    #FileOutW.write(ElemTab_5 + "<gridsysn>Universal Transverse Mercator" + " (ESRI Full Name: " + SR_List["PCSname"] + ")</gridsysn>") #Causes schema error
    FileOutW.write(ElemTab_5 + "<gridsysn>Universal Transverse Mercator</gridsysn>")
    FileOutW.write(ElemTab_5 + "<utm>")
    FileOutW.write(ElemTab_6 + "<utmzone>" + SR_List["UTM_Zone"] + "</utmzone>")
    
    # Transverse Mercator
    # Scale Factor at Central Meridian
    # Longitude of Projection Center
    # Latitude of Projection Center
    # False Easting
    # False Northing
    FileOutW.write(ElemTab_7 + "<transmer>")
    FileOutW.write(ElemTab_8 + "<sfctrmer>" + SR_List["SF"] + "</sfctrmer>") #DI updated
    FileOutW.write(ElemTab_8 + "<longcm>" + SR_List["LongCM"] + "</longcm>") #DI updated
    FileOutW.write(ElemTab_8 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>") #DI updated
    FileOutW.write(ElemTab_8 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_8 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
    FileOutW.write(ElemTab_7 + "</transmer>")
    FileOutW.write(ElemTab_5 + "</utm>")
    FileOutW.write(ElemTab_4 + "</gridsys>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Universal_Polar_Stereographic(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<gridsys>")
    FileOutW.write(ElemTab_5 + "<gridsysn>Universal Polar Stereographic</gridsysn>")#Domain restricted. FGDC requires this (even though our approach below is more informative).
    #FileOutW.write(ElemTab_5 + "<gridsysn>Universal Polar Stereographic" + " (ESRI Full Name: " + SR_List["PCSname"] + ")</gridsysn>")
    
    FileOutW.write(ElemTab_5 + "<ups>")
    FileOutW.write(ElemTab_6 + "<upszone>" + SR_List["UPS_Zone"] + "</upszone>")

    # Straight-Vertical Longitude from Pole
    FileOutW.write(ElemTab_6 + "<svlong>[Unknown]</svlong>") #????????????????????????????????????????

    # ---
    # Standard Parallel
    FileOutW.write(ElemTab_6 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")
    # OR --
    # Scale Factor at Projection Origin
    #FileOutW.write(ElemTab_6 + "<sfprjorg>" + x + "</sfprjorg>") #????????????????????????????????????????
    # ---

    # False Easting
    # False Northing
    FileOutW.write(ElemTab_6 + "<feast>" + SR_List["FE"] + "</feast>")
    FileOutW.write(ElemTab_6 + "<fnorth>" + SR_List["FN"] + "</fnorth>")

    FileOutW.write(ElemTab_5 + "</ups>")
    FileOutW.write(ElemTab_4 + "</gridsys>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def State_Plane_Coordinate_System(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<gridsys>")
    
    DatumYear = ""
    if "1927" in SR_List["PCSname"]:
        DatumYear = "1927"
    if "1983" in SR_List["PCSname"]:
        DatumYear = "1983"
    FileOutW.write(ElemTab_5 + "<gridsysn>State Plane Coordinate System " + DatumYear + "</gridsysn>")
    #FileOutW.write(ElemTab_5 + "<gridsysn>State Plane Coordinate System" + " (ESRI Full Name: " + SR_List["PCSname"] + ")</gridsysn>")
    
    FileOutW.write(ElemTab_5 + "<spcs>")
    FileOutW.write(ElemTab_6 + "<spcszone>" + SR_List["SPCS_Zone"] + "</spcszone>")


    if SR_List["ProjType"] == "Lambert Conformal Conic" or SR_List["ProjType"] == "Lambert_Conformal_Conic":
        # Lambert Conformal Conic
        # Std paral 1
        # Std paral 2 (if exists)
        # Long of Central Meridian
        # Latitude of Projection Origin
        # False Easting
        # False Northing
        FileOutW.write(ElemTab_7 + "<lambertc>")
        FileOutW.write(ElemTab_8 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")
        if SR_List["SP2"] != "[Unknown]":
            FileOutW.write(ElemTab_8 + "<stdparll>" + SR_List["SP2"] + "</stdparll>")
        else: pass
        FileOutW.write(ElemTab_8 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
        FileOutW.write(ElemTab_8 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
        FileOutW.write(ElemTab_8 + "<feast>" + SR_List["FE"] + "</feast>")
        FileOutW.write(ElemTab_8 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
        FileOutW.write(ElemTab_7 + "</lambertc>")


    # OR ----------------------------
    if SR_List["ProjType"] == "Transverse Mercator" or SR_List["ProjType"] == "Transverse_Mercator":
        # Transverse Mercator
        # Scale Factor at Central Meridian
        # Longitude of Projection Center
        # Latitude of Projection Center
        # False Easting
        # False Northing
        FileOutW.write(ElemTab_7 + "<transmer>")
        FileOutW.write(ElemTab_8 + "<sfctmer>" + SR_List["SF"] + "</sfctmer>")
        FileOutW.write(ElemTab_8 + "<longpc>" + SR_List["LongCM"] + "</longpc>")
        FileOutW.write(ElemTab_8 + "<latprjc>" + SR_List["LatPrjOrigin"] + "</latprjc>")
        FileOutW.write(ElemTab_8 + "<feast>" + SR_List["FE"] + "</feast>")
        FileOutW.write(ElemTab_8 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
        FileOutW.write(ElemTab_7 + "</transmer>")


    # OR ----------------------------
    if SR_List["ProjType"] == "Oblique Mercator" or SR_List["ProjType"] == "Oblique_Mercator":
        # Oblique Mercator
        # Scale Factor at Center Line
        FileOutW.write(ElemTab_7 + "<obqmerc>")
        FileOutW.write(ElemTab_8 + "<sfctrlin>" + SR_List["SF"] + "</sfctrlin>")
        # --
        if SR_List["PrjName"] == "Oblique Line Azimuth": #???????????????????????????????????????
            # Oblique Line Azimuth
            #   Azimuthal Angle
            #   Azimuth Measure Point Longitude
            FileOutW.write(ElemTab_8 + "<obqlazim>")
            FileOutW.write(ElemTab_9 + "<azimangl>[Unknown]</azimangl>") #????????????????????????????????????????????????
            FileOutW.write(ElemTab_9 + "<azimptl>[Unknown]</azimptl>") #????????????????????????????????????????????????
            FileOutW.write(ElemTab_8 + "</obqlazim>")
        # OR
        if SR_List["PrjName"] == "Oblique Line Point": #???????????????????????????????????????
            # Oblique Line Point
            #   (two occurrences of both)??
            #   Oblique Line Latitude
            #   Oblique Line Longitude
            FileOutW.write(ElemTab_8 + "<obqlpt>")
            FileOutW.write(ElemTab_9 + "<obqllat>[Unknown]</obqllat>") #????????????????????????????????????????????????
            FileOutW.write(ElemTab_9 + "<obqllat>[Unknown]</obqllat>") #????????????????????????????????????????????????
            FileOutW.write(ElemTab_9 + "<obqllong>[Unknown]</obqllong>") #????????????????????????????????????????????????
            FileOutW.write(ElemTab_9 + "<obqllong>[Unknown]</obqllong>") #????????????????????????????????????????????????
            FileOutW.write(ElemTab_8 + "</obqlpt>")
        # Longitude of Projection Origin
        # False Easting
        # False Northing
        FileOutW.write(ElemTab_8 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
        FileOutW.write(ElemTab_8 + "<feast>" + SR_List["FE"] + "</feast>")
        FileOutW.write(ElemTab_8 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
        FileOutW.write(ElemTab_7 + "</obqmerc>")
        # ---


    # OR ----------------------------
    if SR_List["PrjName"] == "Polyconic":
        # Polyconic
        # Longitude of Central Meridian
        # Latitude of Projection Origin
        # False Easting
        # False Northing
        FileOutW.write(ElemTab_7 + "<polycon>")
        FileOutW.write(ElemTab_8 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
        FileOutW.write(ElemTab_8 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
        FileOutW.write(ElemTab_8 + "<feast>" + SR_List["FE"] + "</feast>")
        FileOutW.write(ElemTab_8 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
        FileOutW.write(ElemTab_7 + "</polycon>")

    FileOutW.write(ElemTab_5 + "</spcs>")
    FileOutW.write(ElemTab_4 + "</gridsys>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def ARC_Coordinate_System(SR_List):
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<gridsys>")
    FileOutW.write(ElemTab_5 + "<gridsysn>Arc Coordinate System</gridsysn>")#Domain restricted. FGDC requires this (even though our approach below is more informative).
    #FileOutW.write(ElemTab_5 + "<gridsysn>Arc Coordinate System" + " (ESRI Full Name: " + SR_List["PCSname"] + ")</gridsysn>")
    FileOutW.write(ElemTab_5 + "<arcsys>")
    FileOutW.write(ElemTab_6 + "<arczone>" + SR_List["Arc_Zone"] + "</arczone>")

    if SR_List["PrjName"] == "Equirectangular":
        # Equirectangular
        # Std Paral 1
        # Long of central Meridian
        # False Easting
        # False Northing
        FileOutW.write(ElemTab_6 + "<equirect>")
        FileOutW.write(ElemTab_7 + "<stdparll>" + SR_List["SP1"] + "</stdparll>")
        FileOutW.write(ElemTab_7 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
        FileOutW.write(ElemTab_7 + "<feast>" + SR_List["FE"] + "</feast>")
        FileOutW.write(ElemTab_7 + "<fnorth>" + SR_List["FN"] + "</fnorth>")
        FileOutW.write(ElemTab_6 + "</equirect>")


    # OR ---
    if SR_List["PrjName"] == "Azimuthal Equidistant":
        # Azimuthal Equidistant
        # Long of central Meridian
        # Latitude of Projection Origin
        # False Easting
        # False Northing
        FileOutW.write(ElemTab_6 + "<azimequi>")
        FileOutW.write(ElemTab_7 + "<longcm>" + SR_List["LongCM"] + "</longcm>")
        FileOutW.write(ElemTab_7 + "<latprjo>" + SR_List["LatPrjOrigin"] + "</latprjo>")
        FileOutW.write(ElemTab_7 + "<feast>" + SR_List["FE"] + "</feast>")
        FileOutW.write(ElemTab_7 + "<fnorth>" + SR_List["FN"] + "</fnorth>")

    FileOutW.write(ElemTab_6 + "</azimequi>")
    FileOutW.write(ElemTab_5 + "</arcsys>")
    FileOutW.write(ElemTab_4 + "</gridsys>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW

def Other_Grid_System(SR_List):
    # We do not have a way to differentiate between grids and map projections so we have no way to
    #   capture this here--therefore, this will not be handled
    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<planar>")
    FileOutW.write(ElemTab_4 + "<gridsys>")
    FileOutW.write(ElemTab_5 + "<othergrd>")
    FileOutW.write(ElemTab_5 + "[Include name, parameters, and values and citation]")
    FileOutW.write(ElemTab_5 + "</othergrd>")
    FileOutW.write(ElemTab_4 + "</gridsys>")
    #FileOutW.write(ElemTab_3 + "</planar>")
    FileOutW.close()
    del FileOutW


#====================================================================
# Map Projection Planar Coordinate Info for updating XML metadata templates
#====================================================================
def Planar_CoordInfo(myDataType, SR_List):

    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_4 + "<planci>")
    if myDataType == "Raster":
        FileOutW.write(ElemTab_5 + "<plance>row and column</plance>")
    else:
        FileOutW.write(ElemTab_5 + "<plance>coordinate pair</plance>")
    # Not supporting distance and bearing
    FileOutW.write(ElemTab_5 + "<coordrep>")
    FileOutW.write(ElemTab_6 + "<absres>" + SR_List["Absc_res"] + "</absres>")
    FileOutW.write(ElemTab_6 + "<ordres>" + SR_List["Ord_res"] + "</ordres>")
    FileOutW.write(ElemTab_5 + "</coordrep>")
    FileOutW.write(ElemTab_5 + "<plandu>" + SR_List["PCS_Units"] + "</plandu>")
    FileOutW.write(ElemTab_4 + "</planci>")
    FileOutW.write(ElemTab_3 + "</planar>")

    FileOutW.close()
    del FileOutW



#====================================================================
# Map Projection Geodetic Model for updating XML metadata templates
#====================================================================
def Geodetic(SR_List):

    FileOutW = open(OutXML_Tmp, 'a')
    FileOutW.write(ElemTab_3 + "<geodetic>")
    if SR_List["DatumName"] != "[Unknown]":
        FileOutW.write(ElemTab_4 + "<horizdn>" + SR_List["DatumName"] + "</horizdn>")
    else: pass
    FileOutW.write(ElemTab_4 + "<ellips>" + SR_List["SpheroidName"] + "</ellips>")
    FileOutW.write(ElemTab_4 + "<semiaxis>" + SR_List["a"] + "</semiaxis>")
    if float(SR_List["f"]) > 0.0:
        FileOutW.write(ElemTab_4 + "<denflat>" + SR_List["f"] + "</denflat>")
    else:
        # This will cause FGDC Metadata parser to fail because not compliant, but FGDC
        #   does not correctly handle Web Mercator or map projections with a spheroid
        FileOutW.write(ElemTab_4 + "<denflat>Flattening for a sphere-based datum = 0.0. (FGDC requests the denominator of the fraction, 1/f, that equates to this flattening value. This is undefined for this map projection.)</denflat>")
    FileOutW.write(ElemTab_3 + "</geodetic>")
    FileOutW.close()
    del FileOutW


#====================================================================
# Local Map Projections for updating XML metadata templates
#====================================================================
### Local Planar: we will rarely run into this and therefore this program
###   will not handle it. These are for coordinate systems where the z-axix
###   coincides with a plumb line though the origin that locally is aligned
###   with the Earth's surface
### We are not tracking any information of metadata elements for this


#====================================================================
# Vertical Map Projections for updating XML metadata templates
#====================================================================
def Vertical_CS(SR_List):
    # Currently, ArcGIS 10 does not do any vertical coordinate system conversions.
    #   You can define a vertical coordinate system on a dataset, but the software
    #   isn't using the information except when defining the spatial reference
    #   (min/max z, z resolution/tolerance values).
    # A vertical coordinate system (vcs) can be referenced to two different types of surfaces:
    #   spheroidal (ellipsoidal) OR gravity-related (geoidal).
    # Most vertical coordinate systems are gravity-related.
    #
    # VCSdatum = [National Geodetic Vertical Datum of 1929", "North American Vertical Datum of 1988", free text]
    # "Explicit elevation coordinate included with horizontal coordinates", "Implicit coordinate", "Attribute values"


    FileOutW = open(OutXML_Tmp, 'a')

    FileOutW.write(ElemTab_2 + "<vertdef>")
    FileOutW.write(ElemTab_3 + "<altsys>")

    FileOutW.write(ElemTab_4 + "<altdatum>" + SR_List["VCSdatum"] + "</altdatum>")
    FileOutW.write(ElemTab_4 + "<altres>" + SR_List["VCS_res"] + "</altres>")
    FileOutW.write(ElemTab_4 + "<altunits>" + SR_List["VCS_Units"] + "</altunits>")
    FileOutW.write(ElemTab_4 + "<altenc>Explicit elevation coordinate included with horizontal coordinates</altenc>")

    FileOutW.write(ElemTab_3 + "</altsys>")
    FileOutW.write(ElemTab_2 + "</vertdef>")

    FileOutW.close()
    del FileOutW

def Data_Type(desc):

    ### Define type of data set
    if desc.DatasetType == "RasterDataset":
        myDataType = "Raster"
    if desc.DatasetType == "FeatureClass":
        myDataType = "Vector"
    if desc.DatasetType == "ShapeFile": # This does not seem to occur any more, but keep for now
        myDataType = "Vector"
    if desc.DatasetType == "Table":
        myDataType = "Table"
    if desc.DatasetType == "FeatureDataset":
        print "This is a feature dataset.  This tool can only be run on feature classes."
        sys.exit(1)
    if desc.DatasetType == "GeometricNetwork":
        myDataType = "GeometricNetwork"

    ### Define type of shape for non raster datasets
    if myDataType not in ["Raster", "Table", "FeatureDataset", "GeometricNetwork"]:
        if desc.shapeType == "Polygon":
            myFeatType = "Polygon"
        if desc.shapeType == "Polyline":
            myFeatType = "Polyline"
        if desc.shapeType == "Point":
            myFeatType = "Point"
        if desc.shapeType == "MultiPoint" or desc.shapeType == "Multipoint":
            myFeatType = "Point"
    elif myDataType == "Raster":
        myFeatType = "None"
    elif myDataType == "Table":
        myFeatType = "None"
    elif myDataType == "FeatureDataset":
        myFeatType = "None"
    elif myDataType == "GeometricNetwork":
        myFeatType = "None"

    ### Return desired objects
    return myDataType, myFeatType   
#############################################################################################
##Testing
#installInfo = arcpy.GetInstallInfo()
#installDir = installInfo["InstallDir"]
#GCS_PrjFile = os.path.join(installDir, r"Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj")
#InDS = r"C:\temp\MetadataWizard\CO_NM_AssessmentUnits.shp"
#WorkingDir = r"c:\temp\MetadataWizard"
#GCS_ExtentList = Get_LatLon_BndBox()[1]
#SpatialRefInfo(GCS_PrjFile, InDS, WorkingDir, GCS_ExtentList)


def SpatialRefInfo(GCS_PrjFile, InDS, WorkingDir, GCS_ExtentList):
    
    desc = arcpy.Describe(InDS)
    global OutXML_Tmp
    OutXML_Tmp = os.path.join(WorkingDir, "SpatialRef.xml")

    if os.path.exists(OutXML_Tmp):
        os.remove(OutXML_Tmp)

    myDataType = Data_Type(desc)[0]
    myFeatType = Data_Type(desc)[1]
    
    SR_InDS = desc.SpatialReference    
    SR_List = Get_SpatialRef(SR_InDS, myDataType, myFeatType, GCS_ExtentList, desc, InDS)
    XML_SpatialReference(SR_List, myDataType)
    
    SpRefFile = open(OutXML_Tmp)
    SpRefString = SpRefFile.read()
    SpRefFile.close
    del SpRefFile
    os.remove(OutXML_Tmp)
    return SpRefString




