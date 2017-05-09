"""
Author:  Drew Ignizio
Created:  04/26/2012
Script Purpose/Notes:

A general suite of functions to support the Metadata Wizard tool.

These tools anticipate input XML files being in FGDC format. They can be expected
to generate erroneous results or fail in non-FGDC records.

"""
import traceback
import os, sys, subprocess, time, stat
import arcpy 
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
import fileinput
import re
import shutil
import math
import xml.etree.ElementTree as ET

def CreateCopyMDRecord(InputXML_or_DataLayer, MDRecordCopy): #Creates unmodified backup of input.
    '''
    Obtains the raw metadata from a dataset. This makes an exact copy.
    '''

    #Finds the install directory and obtains the xslt used to grab all of the xml contents, unedited
    installDir = arcpy.GetInstallInfo("desktop")["InstallDir"]
    xsltPath = "Metadata/Stylesheets/gpTools/exact copy of.xslt"
    Exact_Copy_XSLT = os.path.join(installDir,xsltPath)
    Exact_Copy_XSLT = os.path.realpath(Exact_Copy_XSLT)
    
    #Process: Get Metadata
    try:
        if os.path.exists(MDRecordCopy):
            os.remove(MDRecordCopy)
    except IOError:
        raise Exception, "This tool requires read/write access to the directories where the temporary and final outputs are saved. Please choose another directory for the tool outputs."
    
    try:  
        arcpy.XSLTransform_conversion(InputXML_or_DataLayer, Exact_Copy_XSLT, MDRecordCopy)
    except:
        raise Exception, str(arcpy.GetMessages(2))

def RemoveNameSpace(MDFile):#Eliminate namespace tags from root element in xml if present (appear when ExportFGDC is run on spatial data sets).
    
    #Will eliminate namespace noise like "<metadata xmlns:fn=...>" Convert to simply '<metadata>'.
    try:
        Metafile = open(MDFile,'r')
        MetafileLines = Metafile.readlines()
        Metafile.close
        MetafileClean = open(MDFile, 'w')
        
        for line in MetafileLines:
            if "<metadata xmlns" in line:
                line = "<metadata>"
            MetafileClean.write(line)
        MetafileClean.close
    except: 
        pass
    
def RemoveStyleSheet(MDFile):

    #Will remove the stylesheet added in the VB.Net editor that gets added to facilitate the MD Preview
    try:
        Metafile = open(MDFile,'r')
        MetafileLines = Metafile.readlines()
        Metafile.close
        MetafileClean = open(MDFile, 'w')
        
        for line in MetafileLines:
            if "<?xml-stylesheet href" in line:
                line = ""
            MetafileClean.write(line)
        MetafileClean.close
    except:
        pass

def CheckMasterNodes(XMLfile):
    '''
    This function will ensure that the 7 key element nodes of an FGDC-CSDGM record are present.
    If they are not found, the routine will add them to the input XML file.
    '''
    masterNodeList = ['idinfo', 'dataqual', 'spdoinfo', 'spref', 'eainfo', 'distinfo', 'metainfo']
    missingNodes = []
    
    etree = ET.ElementTree(file=XMLfile)
    root = etree.getroot()
    
    for iNode in masterNodeList:
        if etree.find(iNode) == None:
            missingNodes.append(iNode)
            
    for xNode in missingNodes:
        insertNode = ET.Element(xNode)
        root._children.insert(-1, insertNode)
    
    etree.write(XMLfile)    
    
def removeNodeByName(XMLfile, NodeName):
    '''
    Will remove all instances of a node by a certain 'name' in an xml document.
    See example at: http://drumcoder.co.uk/blog/2010/jun/17/using-elementtree-python/
    The method used to remove elements in the other routines (WriteEAInfo, WriteSpatialRefInfo, WriteSpatialDataOrgInfo) will remove just the first found instance.
    (This code works based on this import construct: "import xml.etree.ElementTree as ET")
    '''
    lDocument = ET.ElementTree()
    lDocument.parse(XMLfile)
    lRoot = lDocument.getroot()
    lRemoveList = []

    for child in lRoot.findall(NodeName):#NodeName would be passed as 'eainfo', for example
        print child
        lRemoveList.append(child)

    for child in lRemoveList:
        lRoot.remove(child)
    
    lDocument.write(XMLfile)

def replaceXMLNodeContents(XMLfile, NodePath, NewNodeContents, addifmissing=True):#Will gut and replace a node with new, nested XML contents.
    '''
    Inputs:
    1. Full path to XML file to modify.
    2. The path to the node whose contents will be replaced. Skip root element in path (e.g. "idinfo/citation" or "spref", don't include "metadata" for FGDC).
    3. A string representation of well-formatted XML content.
        Example:'<samplenode><innernode><pocketcontent1>PC1</pocketcontent1><pocketcontent2>PC2</pocketcontent2></innernode></samplenode>'
    
    '''
    etree = ET.ElementTree(file=XMLfile)
    NodeContent = ET.XML(NewNodeContents)#Converts a string representing XML content to a well-formatted XML node object. This chokes if string has two root elements!
    
    if etree.find(NodePath)!= None:
        stub = etree.find(NodePath)
        stub.clear()
        stub.insert(0, NodeContent)
    
    elif addifmissing:
        missingNodes = []
        while etree.find(NodePath)== None: #While the path to an element can't be found...
            
            arcpy.AddMessage("'" + str(NodePath) + "'" + " could not be found. The element will now be added and populated...")
            
            pathnodes = NodePath.split("/") #Split the path into a list of nodes.
            missingNodes.insert(0, pathnodes[-1])#Create a list of nodes we can't find. Start with the lowest node and work up.
            NodePath = "/".join(pathnodes[:-1])#Try again higher up trunk of tree. The new parent node string becomes the string minus the last node.
         
        for node in missingNodes:
            stub = etree.find(NodePath)
            nodeAdd = ET.Element(str(node))
            stub.insert(0, nodeAdd)#This inserts the new element as the first child.
            NodePath = NodePath + ("/" + node)#Rebuild the full path to the node we originally wanted to edit.
        
        stub = etree.find(NodePath)
        stub.clear()
        stub.insert(0, NodeContent)
    
    else:
        raise RuntimeError, "Unable to update the XML file. Check that the file exists, the provided node-path within the XML, or permission settings."
        
    etree.write(XMLfile)
    #etree.write(r"C:\temp\MetadataWizard\bc_int_FGDCxxxx.xml")
       
def changeXMLNodeText(XMLfile, path, text, addifmissing=True):#Updates the text content of an XML element, specified by full address/path.
    
    '''
    Inputs:
    1. XML file metadata record.
    2. The full path to the element which needs to have its content edited, skipping the Root. (Example: "idinfo/citation/citeinfo/origin")
    3. The text to replace the current content. 
    4. addifmissing True/False toggle to build out to element when not found. Defaults to True.
    
    By default the function will attempt to build out to the full path and update the text.
    '''
    
    etree = ET.ElementTree(file=XMLfile)

    if etree.find(path)!= None:
        targetNode = etree.find(path)
        targetNode.text = text

    elif addifmissing:

        missingNodes = []
        while etree.find(path)== None: #While the path to an element can't be found...
            
            pathnodes = path.split("/") #Split the path into a list of nodes.
            missingNodes.insert(0, pathnodes[-1])#Create a list of nodes we can't find. Start with the lowest node and work up.
            path = "/".join(pathnodes[:-1])#Try again higher up trunk of tree. The new parent node string becomes the string minus the last node.
         
        for node in missingNodes:
            stub = etree.find(path)
            nodeAdd = ET.Element(str(node))
            stub.insert(0, nodeAdd)#This inserts the new element as the first child.
            path = path + ("/" + node)#Rebuild the full path to the node we originally wanted to edit.

        targetNode = etree.find(path)
        targetNode.text = text 
       
    else:
        raise RuntimeError, "Unable to update the XML file. Check that the file exists, the provided node-path within the XML, or permission settings."
    
    etree.write(XMLfile)
    
def WriteNativeEnvInfo(MDFile, NativeInfo):
    try:
        changeXMLNodeText(MDFile, "idinfo/native", str(NativeInfo), addifmissing=True)
        arcpy.AddMessage("Updating 'Native Environment' information...\n")
    except:
        arcpy.AddMessage("Unable to update 'Native Environment' information. Investigate this element in finished record. \n")

def WriteMDDate(MDFile, MDDate):
    try:
        changeXMLNodeText(MDFile, "metainfo/metd", str(MDDate), addifmissing=True)
        arcpy.AddMessage("Updating 'Metadata Info (Date)' information...\n")
    except:
        arcpy.AddMessage("Unable to update 'Metadata Info (Date)' information. Investigate this element in finished record. \n")      
    
   
def WriteBoundingInfo(MDFile, WestBC, EastBC, NorthBC, SouthBC):#Update the bounding information of a spatial data set.
    
    try:#Update each bounding coordinate element.
        if str(WestBC) == "nan":
            WestBC = "-180"
        if str(EastBC) == "nan":
            EastBC = "180"
        if str(NorthBC) == "nan":
            NorthBC = "90"
        if str(SouthBC) == "nan":
            SouthBC = "-90"
            
            
        changeXMLNodeText(MDFile, "idinfo/spdom/bounding/westbc", str(WestBC), addifmissing=True)
        changeXMLNodeText(MDFile, "idinfo/spdom/bounding/eastbc", str(EastBC), addifmissing=True)
        changeXMLNodeText(MDFile, "idinfo/spdom/bounding/northbc", str(NorthBC), addifmissing=True)
        changeXMLNodeText(MDFile, "idinfo/spdom/bounding/southbc", str(SouthBC), addifmissing=True)
        #Note: If they are not found, this will effectively add the elements in a way that results in their inversion (because each one is pushed down, in order).
        #This is resolved via re-running FGDC translator downstream.
        arcpy.AddMessage("Updating 'Bounding Coordinates' values...\n")
                    
    except:
        arcpy.AddMessage("Unable to update bounding box information. Investigate this element in finished record. \n")

def WriteGeospatialForm(MDFile, DataType, FeatType):#Update the Geospatial Data Presentation form of a spatial data set and Format Name in Dist. Info
    #Possible Data Types: 'XML File', 'Raster', 'Vector', 'Table', 'GeometricNetwork'
    #A check is performed; this routine is skipped for XML inputs to tool ('XML File')
    
    if DataType in ["Raster", "Vector", "GeometricNetwork"]:
        if FeatType != "None":
            GeoForm = DataType + " Digital Data Set" + " (" + FeatType + ")" #
        else:
            GeoForm = DataType + " Digital Data Set" #'Raster Digital Data Set', 'GeometricNetwork Digital Data Set'

    elif DataType == "Table":
        GeoForm = "Tabular Digital Data"

    try:#Look for and try to replace "GeoForm" element.   
        changeXMLNodeText(MDFile, "idinfo/citation/citeinfo/geoform", str(GeoForm), addifmissing=True)
        arcpy.AddMessage("Updating 'Geospatial Presentation Form' with: " + str(GeoForm) + "\n")

    except:
        arcpy.AddMessage("Unable to update the 'Geospatial Presentation Form.' Investigate this element in finished record. \n")
        
    try:#Look for and try to replace "Digital Transfer Info - Format Name" element.   
        changeXMLNodeText(MDFile, "distinfo/stdorder/digform/digtinfo/formname", str(GeoForm), addifmissing=True)
        arcpy.AddMessage("Updating 'Digital Transfer Info - Format Name' with: " + str(GeoForm) + "\n")

    except:
        arcpy.AddMessage("Unable to update 'Digital Transfer Info - Format Name.' Investigate this element in finished record. \n")

def WriteSpatialDataOrgInfo(MDFile, SpDoInfo):#Update the Spatial Data Organization Info of a spatial data set.
    
    etree = ET.ElementTree(file=MDFile)
    #root = etree.find("")###!!!!!!
    root = etree.getroot()
    
    if etree.find("spdoinfo")!= None: #If "Spatial Data Organization Info" is found, delete it.
        targetNode = etree.find("spdoinfo")
        root.remove(targetNode)  
        
    try:
        SpDoInfo = ET.XML("<spdoinfo>" + str(SpDoInfo) + "</spdoinfo>")
        root.insert(-1, SpDoInfo)#Add new element at the end. We'll fix the order issue by re-running FGDC translator.
        etree.write(MDFile)
        arcpy.AddMessage("Updating 'Spatial Data Organization Info' element...\n")       
        
    except:
        arcpy.AddMessage("Unable to update 'Spatial Data Organization Info'. Investigate this element in finished record. \n")

def WriteSpatialRefInfo(MDFile, SpatialRefInfo):#Update the Spatial Reference Info of a spatial data set.
    
    etree = ET.ElementTree(file=MDFile)
#    root = etree.find("")
    root = etree.getroot()
    
    if etree.find("spref")!= None: #If "Spatial Reference Info" is found, delete it.
        targetNode = etree.find("spref")
        root.remove(targetNode)  
    
    try: 
        SpRef = ET.XML(str(SpatialRefInfo))
        root.insert(-1, SpRef)#Add new element at the end. We'll fix the order issue by re-running FGDC translator.
        etree.write(MDFile)
        arcpy.AddMessage("Updating 'Spatial Reference Info' element...\n")
    except:
        arcpy.AddMessage("Unable to update the 'Spatial Reference Info.' Investigate this element in finished record. \n")

def RetrieveEAInfo(EAtextfile):#Retrieve the Entity/Attribute info generated by the EA tool as string from text file created in Working Directory.
    EAfile = open(EAtextfile)
    EAstring = EAfile.read()
    EAfile.close
    del EAfile
    os.remove(EAtextfile)
    return EAstring

def WriteEAInfo(MDFile, EAInfo):#Update the Entity and Attribute Info of a spatial data set.
    
    etree = ET.ElementTree(file=MDFile)
    #root = etree.find("")
    root = etree.getroot()
    
    if etree.find("eainfo")!= None: #If Entity/Attribute Info" is found, delete it.
        targetNode = etree.find("eainfo")
        root.remove(targetNode)  
    
    try:  
        EAInfo = ET.XML(str(EAInfo))
        root.insert(-1, EAInfo)#Add new element at the end. We'll fix the order issue by re-running FGDC translator.
        etree.write(MDFile)
        arcpy.AddMessage("Updating 'Entity and Attribute Info' element...\n")
    except:
        arcpy.AddMessage("Unable to update the 'Entity and Attribute Info.' Investigate this element in finished record. \n")


def ReRunFGDCTranslator(InputXML):
    #Implement the USGSMPTranslator tool to re-export the FGDC record. 
    #This should fix the problem of any child elements being in the wrong order.
    #User will need write access to wherever the input is coming from. Input is replaced with output.
    OutputXML = os.path.splitext(InputXML)[0] + "xx.xml"
  
    try:
        if os.path.exists(OutputXML):
            os.remove(OutputXML) 
    except:
        raise Exception, "Error. This tool requires read/write access to the directories where the temporary and final outputs are saved. Please choose another directory for the tool outputs."
    
    arcpy.USGSMPTranslator_conversion(InputXML, "#", "xml", OutputXML)
    os.remove(InputXML)#Remove original input
    shutil.copy(OutputXML, InputXML)#Copy re-ordered output ("_xx.xml" file) back to original input file location.
    os.remove(OutputXML)#Get rid of re-ordered tool output ("_xx.xml" file).

def ReplaceXML(OldXML, NewXML):
    #Simply replaces one XML with a new one. The new XML file will end up with the same name as the old one it replaced.
    #Routine is skipped if no '...temp.xml' has been saved from the stand-alone editor.
    if os.path.exists(NewXML):
        os.remove(OldXML)#Remove original input
        shutil.copy(NewXML, OldXML)#Copy re-ordered output ("_temp.xml" file) back to original input file location.
        os.remove(NewXML)#Get rid of re-ordered tool output ("_temp.xml" file).

def SendToOnlineEditor():
    pass
#URL = r"http://mercury.ornl.gov/OME/"
#webbrowser.open(URL)
#
#subprocess.Popen('"C:\\Program Files\\Internet Explorer\\iexplore.exe" http://www.google.com')


    
if __name__ == '__main__':
    
    
#    Test some things

    print "Script completed."
    

        
    
    
    