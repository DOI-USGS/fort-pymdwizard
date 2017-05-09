'''
Created April 2011

This tool was developed by Colin Talbert and Drew Ignizio at the USGS Fort Collins Science Center (FORT).

http://www.fort.usgs.gov/


'''
import xml.dom
from xml.dom import minidom
import xml
import arcpy
import os
import sys
import codecs
import shutil

arcpy.env.overwriteOutput = True

'''
This code requires 2 inputs: 
    A)An input data layer (complete with metadata) or a raw xml metadata record. *As of now, this tool can handle only records in FGDC and Arc10 format.
    
    B)A user-defined name and output directory for the resulting cleaned FGDC-style metadata record. This output is an xml file.
    (This output file may still be missing elements/element values and need additional editing, however this code handles the conversion and some 
    preliminary cleaning automatically.)

Processing Steps: 
1. The code will use an Arcpy style sheet to obtain an exact copy of the entire xml. This will ensure that despite what is
    shown in ArcCatalog (the ESRI format can hide some elements), all the elements that are present in the file will be considered.

2. This raw xml file is then parsed and a series of tests are employed to determine if the format of the xml file is Arc10 or
    FGDC. This code is currently only equipped to handle xml files that are in one of these two formats.

3. A series of tests is performed to determine the format of the metadata record (these tests look at the structure and content of the xml for
    characteristics unique to a particular formatting type).
    
    If the xml file is determined to be in Arc10 format:
    -The file is run through the ESRI metadata translator ("ARCGIS2FGDC") to  be converted to an FGDC style record. 
    
    If the xml file is determined to be in FGDC format:
    -The file is run through the USGS MP Translator (to FGDC) tool. This is effectively an FGDC-to-FGDC operation but must be used since ESRI
    does not provide an "FGDC TO FGDC" option in their metadata translator tool. This allows a user to export an FGDC-style xml for editing.
    
4. The file is then cleaned to remove the ' Sync="TRUE"' elements that are generated during the translation process and any auto-populated ESRI
    reminder elements (e.g., "REQUIRED: The name of an organization or individual that developed the data set." or 
    "REQUIRED: The date when the data set is published or otherwise made available for release.") These are removed so that when MP or other QA/QC
    checks are run on the xml file, an error will actually be generated at this element to remind a user that the value needs to be populated.
'''

def GetRawXML(InputXML_or_DataLayer, OutputRawXML):
    '''
    Obtains the raw metadata from a dataset.
    '''

    #Finds the install directory and obtains the xslt used to grab all of the xml contents, unedited
    installDir = arcpy.GetInstallInfo("desktop")["InstallDir"]
    xsltPath = "Metadata/Stylesheets/gpTools/exact copy of.xslt"
    Exact_Copy_XSLT = os.path.join(installDir,xsltPath)
    Exact_Copy_XSLT = os.path.realpath(Exact_Copy_XSLT)
    arcpy.AddMessage("The raw xml is now being extracted into a temporary file for further processing... \n")
    
    #Process: Get Metadata
    try:
        if os.path.exists(OutputRawXML):
            os.remove(OutputRawXML)
    except IOError:
        raise Exception, "Error. This tool requires read/write access to the directories where the temporary and final outputs are saved. Please choose another directory for the tool outputs."
    
    try:  
        arcpy.XSLTransform_conversion(InputXML_or_DataLayer, Exact_Copy_XSLT, OutputRawXML)
        #arcpy.AddMessage(arcpy.GetMessages(0))
    except:
        raise Exception, str(arcpy.GetMessages(2))
        
def DetermineMDType(RawXMLFile):
    '''
    A series of tests is performed to determine the format of the metadata record (these tests look at the structure and content
    of the xml for characteristics unique to certain formatting).
    '''    
    dom = minidom.parse(RawXMLFile)
    XMLElements = [node.tagName for node in dom.getElementsByTagName("*")]
    arcpy.AddMessage("A series of tests will now be performed to determine the current format of the metadata record... \n")
    
#Check 1. Determine if metadata contains information identifying it as being an Arc10 style record.
    if "mdStanName" in XMLElements:
        dom = minidom.parse(RawXMLFile)
        mdStanName = dom.getElementsByTagName('mdStanName')[0].firstChild.data
        
        if str(mdStanName) == "ArcGIS Metadata":
            arcpy.AddMessage("The 'mdStanName' element was found in the data layer and contains the value 'ArcGIS Metadata.' This data layer has been determined to have Arc10 style Metadata. \n")
            del dom
            return "Arc10" 
        else: 
            arcpy.AddMessage("The 'mdStanName' element was found in the data layer but did not contain the value 'ArcGIS Metadata.' Subsequent checks will be performed to determine the format of the metadata. \n")
        
    #else: print "The element 'mdStanName' was not found in the XML file. Subsequent checks will be performed to determine the format of the metadata. \n"

#Check 2. Determine if metadata has 1 or more of several elements unique to Arc10 style metadata records.
    KeyElementCheckList = ["idPurp", "idAbs", "idCredit", "searchKeys"]
    KeyElementCounter = 0
    for KeyElement in KeyElementCheckList:
        if KeyElement in XMLElements:
            KeyElementCounter = KeyElementCounter + 1
    if KeyElementCounter > 0:
        arcpy.AddMessage("Out of 4 elements unique to Arc10 style metadata ('idPurp,' idAbs,' idCredit,' and 'searchKeys') " + str(KeyElementCounter) + " were found. This data layer has been determined to have Arc10 style metadata. \n")
        #print "MetadataType Variable = " + MetadataType
        return "Arc10"
   
# else: print "Of 4 elements unique to Arc10 style metadata, none could be found. Subsequent checks will be performed to determine the format of the metadata. \n"
        
#Check 3. Determine if metadata has 1 or more of several elements unique to FGDC style records, in a particular structure.
    try:
        idinfo = dom.getElementsByTagName("idinfo")[0]
        citation = idinfo.getElementsByTagName('citation')[0]
        citeinfo = citation.getElementsByTagName('citeinfo')[0]
        
        metainfo = dom.getElementsByTagName("metainfo")[0]
        metstdn = metainfo.getElementsByTagName("metstdn")[0]
        
        if not citeinfo is None and not metstdn is None:
            arcpy.AddMessage("Based on certain characteristics of the xml, this metadata record has been identified as an FGDC-style record. \n")
            return "FGDC"
        else:
            return "Unknown"
        
    except:
        return "Unknown"
 


def ConvertArc10toFGDC(SourceFile, OutputXML_inFGDCFormat, TempDir):
        #print "Metadata type is 'Arc10.' Converting Arc10 metadata file to FGDC via USGS MP Translator tool and saving to xml..."
        #Find the ArcGis to FGDC Translator based on the install directory of the machine.
        installDir = arcpy.GetInstallInfo("desktop")["InstallDir"]
        TranslatorPath = "Metadata/Translator/ARCGIS2FGDC.xml"
        Translator = os.path.join(installDir, TranslatorPath)
        arcpy.AddMessage("Now converting the Arc10 record to an FGDC-style xml file...")
        
        #Export ArcGIS10 metadata to FGDC style
        try:
            if os.path.exists(OutputXML_inFGDCFormat):
                os.remove(OutputXML_inFGDCFormat)
        except:
            raise Exception, "Error. This tool requires read/write access to the directories where the temporary and final outputs are saved. Please choose another directory for the tool outputs."
        
        try:
            #arcpy.ESRITranslator_conversion(SourceFile, Translator, OutputXML_inFGDCFormat)
            #This is causing problematic locks... steps below should avoid trouble.
            
            TranslateOut = os.path.join(TempDir, "ArcpyTranslate.xml")
            if os.path.exists(TranslateOut):
                os.remove(TranslateOut)
            arcpy.ESRITranslator_conversion(SourceFile, Translator, TranslateOut)
            arcpy.AddMessage(arcpy.GetMessages(0))
            
            shutil.copy(TranslateOut, OutputXML_inFGDCFormat)
            
        except:
            raise Exception, arcpy.AddError(arcpy.GetMessages(2))
        
        arcpy.AddMessage("\n")
        arcpy.AddMessage("Metadata converted successfully.")

def ExportFGDCtoFGDC(InputXMLFile, OutputXMLFile):
    try:
        if os.path.exists(OutputXMLFile):
            os.remove(OutputXMLFile) 
    except:
        raise Exception, "Error. This tool requires read/write access to the directories where the temporary and final outputs are saved. Please choose another directory for the tool outputs."
    
#Implement the USGSMPTranslator tool to export to FGDC (effectively, this is an FGDC to FGDC translation). 
#Usage: USGSMPTranslator_conversion (source, config, conversion, output, error log)     
    arcpy.USGSMPTranslator_conversion(InputXMLFile, "", "xml", OutputXMLFile)

def CleanESRIFGDC(InputXMLFile, outputXMLFile): 
    '''   
    This routine takes an .xml and removes formatting introduced by ESRI at 9.3 and earlier.
    The elements which are removed are the 'Sync = TRUE' attributes
    and any of the "Required: ..." auto-added ESRI FGDC hints.
    
    '''        
    arcpy.AddMessage("The FGDC-style record has been exported an output xml file in FGDC format and is now being cleaned...")
    try:
        if os.path.exists(outputXMLFile):
            os.remove(outputXMLFile) 
    except:
        raise Exception, "Error. This tool requires read/write access to the directories where the temporary and final outputs are saved. Please choose another directory for the tool outputs."
    
    inputDOM = minidom.parse(InputXMLFile)
    changed = False
    for node in inputDOM.getElementsByTagName("*"):
        #print node.tagName
        try:
            nodeValue = node.firstChild.data
        except AttributeError:
            pass
            
        try:
            node.removeAttribute('Sync')
            changed = True            
        except xml.dom.NotFoundErr:
            pass
        
        if nodeValue[0:10] == "REQUIRED: ":
            changed = True
            nodeName = node.tagName
            arcpy.AddMessage("The node '" + nodeName + "' has value: " + nodeValue)
            arcpy.AddMessage("This is an auto-generated ESRI value. The value will now be be deleted... \n")
            contents = node.firstChild
            newContents = inputDOM.createTextNode("")
            node.replaceChild(newContents, contents)
              
    if changed:
        EncodingType = str(inputDOM.encoding)
        if EncodingType == 'None':
            EncodingType = "UTF-8"
        fileObj = codecs.open(outputXMLFile, "w", EncodingType )
        inputDOM.writexml(fileObj, "", encoding=EncodingType)
        #PrettyXML = inputDOM.toprettyxml()
        #fileObj.write(PrettyXML)
        fileObj.close()
        os.remove(InputXMLFile)
        arcpy.AddMessage("\nConversion complete.")
    else:
        shutil.copy(InputXMLFile, outputXMLFile)
        os.remove(InputXMLFile)
        
    arcpy.AddMessage("...cleaning completed.\n")
''' 
def GetMDContent(argv):#string of args
    sourceDataFile = argv[1]
    sourceFile = os.path.split(os.path.splitext(sourceDataFile)[0])[1]
    OutputFGDCXML = argv[2]
''' 
def GetMDContent(sourceDataFile, OutputFGDCXML, TempDir):
    
    sourceFile = os.path.split(os.path.splitext(sourceDataFile)[0])[1]
    '''
    #we save our intermediate step into the same location as the input
    #this would raise an error if they don't have write permission here.
    # if default output workspace is a geodatabase
    # move output to folder path above it
    #tmpOutDir = os.path.dirname(sourceDataFile)
    
    DI: Not applicable. Working directory is now used.
    '''
    tmpOutDir = os.path.dirname(OutputFGDCXML)#Temp working files will be saved in 'Working Dir' with this tool.
    while (".mdb" in tmpOutDir or ".gdb" in tmpOutDir):
        tmpOutDir = os.path.dirname(tmpOutDir)
    tmpXML = os.path.join(tmpOutDir, sourceFile + ".tmp.xml")

    # make sure extension is ".xml"
    lstPath = os.path.splitext(OutputFGDCXML)
    if lstPath[1].lower() != ".xml":
        OutputFGDCXML = lstPath[0] + ".xml"

    GetRawXML(sourceDataFile, tmpXML)
    try:
        metadataType = DetermineMDType(tmpXML)
        
        if metadataType == "FGDC":
            ExportFGDCtoFGDC(sourceDataFile, tmpXML)
            CleanESRIFGDC(tmpXML, OutputFGDCXML)
        elif metadataType == "Arc10":
            arcpy.SynchronizeMetadata_conversion(sourceDataFile, "ALWAYS")
            ConvertArc10toFGDC(sourceDataFile, OutputFGDCXML, TempDir)
        elif metadataType == "Unknown":
            raise Exception, "The format of the metadata could not be determined. Possible explanations include: the data layer is missing metadata, the metadata is a malformed xml, or the metadata record is in a format other than FGDC or ESRI. Please investigate the record visually or recreate the metadata record. If the record is intact, try converting it to FGDC or ESRI format before using this tool."      
    finally:
        if os.path.exists(tmpXML):
                os.remove(tmpXML)

#if __name__ == '__main__':
#    GetMDContent(sys.argv)  #This would run the script from this .py file, in conjunction with the commented out 4 lines of GetMDContent above.


