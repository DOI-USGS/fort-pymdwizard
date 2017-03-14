#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for a SRCInfo <srcinfo> section


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

from lxml import etree

from PyQt5.QtGui import QPainter, QFont, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLineEdit, QSizePolicy, QComboBox, QTableView, QFormLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPlainTextEdit, QRadioButton, QFrame
from PyQt5.QtWidgets import QStyleOptionHeader, QHeaderView, QStyle, QScrollArea, QGroupBox
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSize, QRect, QPoint



from pymdwizard.core import utils
from pymdwizard.core import xml_utils

from pymdwizard.gui.wiz_widget import WizardWidget
from pymdwizard.gui.ui_files import UI_SRCInfo #
from pymdwizard.gui.single_date import SingleDate
from pymdwizard.gui.Citation import Citation
from pymdwizard.gui.timeperd import Timeperd



class SRCInfo(WizardWidget): #

    drag_label = "SRCInfo <srcinfo>"


    def build_ui(self):
        """
        Build and modify this widget's GUI

        Returns
        -------
        None
        """
        self.ui = UI_SRCInfo.Ui_Form()
        self.ui.setupUi(self)
        self.timeperd = Timeperd()
        self.citation = Citation(parent=self, include_lwork=False)


        self.citation.ui.fgdc_lworkcit.deleteLater()
        self.ui.frame_citation.layout().addWidget(self.citation)
        self.ui.frame_timeperd.layout().addWidget(self.timeperd)

        self.setup_dragdrop(self)




    def connect_events(self):
        """
        Connect the appropriate GUI components with the corresponding functions

        Returns
        -------
        None
        """



    def dragEnterEvent(self, e):
        """
        Only accept Dragged items that can be converted to an xml object with
        a root tag called 'srcinfo'

        Parameters
        ----------
        e : qt event

        Returns
        -------
        None

        """
        print("pc drag enter")
        mime_data = e.mimeData()
        if e.mimeData().hasFormat('text/plain'):
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            element = etree.fromstring(mime_data.text(), parser=parser)
            if element.tag == 'srcinfo':
                e.accept()
        else:
            e.ignore()


         
                
    def _to_xml(self):
        """
        encapsulates the QLineEdit text in an element tag

        Returns
        -------
        srcinfo element tag in xml tree
        """
        srcinfo = xml_utils.xml_node('srcinfo')
        srccite = xml_utils.xml_node('srccite', parent_node=srcinfo)

        cite = self.citation._to_xml()
        srccite.append(cite)

        srcscale = xml_utils.xml_node('srcscale',
                                      text = self.ui.fgdc_srcscale.text(),
                                      parent_node=srcinfo)
        typesrc = xml_utils.xml_node('typesrc',
                                      text = self.ui.fgdc_typesrc.currentText(),
                                      parent_node=srcinfo)

        srctime = xml_utils.xml_node('srctime', parent_node=srcinfo)
        time = self.timeperd._to_xml()
        timeinfo = time.xpath('/timeperd/timeinfo')[0]
        srctime.append(timeinfo)

        #srccurr = xml_utils.xml_node('srccurr', parent_node=srctime)
        cur = time.xpath('/timeperd/current')[0]
        cur.tag = 'srccurr'
        srctime.append(cur)

        srccitea = xml_utils.xml_node('srccitea',
                                      text = self.ui.fgdc_srccitea.text(),
                                      parent_node=srcinfo)

        srccontr = xml_utils.xml_node('srccontr',
                                      text = self.ui.fgdc_srccontr.text(),
                                      parent_node=srcinfo)

        return srcinfo

    def _from_xml(self, srcinfo):
        """
        parses the xml code into the relevant srcinfo elements

        Parameters
        ----------
        srcinfo - the xml element status and its contents

        Returns
        -------
        None
        """
        try:
            if srcinfo.tag == "srcinfo":
                # print srcinfo.tag
                utils.populate_widget(self, srcinfo)
                srccite = srcinfo.xpath('srccite')[0]
                citeinfo = srccite.xpath('citeinfo')[0]
            elif srcinfo.tag != 'srcinfo':
                print("The tag is not 'srcinfo'")
                return

            #self.citation._from_xml(srccite.xpath('citeinfo')[0])

            utils.populate_widget_element(self.citation.ui.fgdc_title, citeinfo, 'title')

            utils.populate_widget_element(self.citation.ui.pubdate_widget.ui.lineEdit,
                                          citeinfo, 'pubdate')

            self.citation.fgdc_origin.clear_widgets()
            if citeinfo.findall("origin"):
                for origin in citeinfo.findall('origin'):
                    origin_widget = self.citation.fgdc_origin.add_another()
                    origin_widget.added_line.setText(origin.text)
            else:
                self.citation.fgdc_origin.add_another()

            self.citation.onlink_list.clear_widgets()
            if citeinfo.findall("onlink"):
                for onlink in citeinfo.findall('onlink'):
                    onlink_widget = self.citation.onlink_list.add_another()
                    onlink_widget.added_line.setText(onlink.text)
            else:
                self.citation.onlink_list.add_another()

            if citeinfo.xpath('serinfo'):
                self.citation.ui.radio_seriesyes.setChecked(True)
                serinfo = srcinfo.xpath('srccite/citeinfo/serinfo/serinfo')[0].text
                self.citation.ui.fgdc_sername.setText(str(serinfo))
                issue = srcinfo.xpath('srccite/citeinfo/serinfo/issue')[0].text
                self.citation.ui.fgdc_issue.setText(str(issue))
               ## utils.populate_widget(self.citation.ui.fgdc_serinfo, citeinfo.xpath('serinfo')[0])
                # utils.populate_widget(self.citation.ui.fgdc_publish, srcinfo.xpath('srccite/citeinfo/pubinfo')[0])
            else:
                self.citation.ui.radio_seriesyes.setChecked(False)

            if citeinfo.xpath('pubinfo'):
                self.citation.ui.radio_pubinfoyes.setChecked(True)
                pubplace = srcinfo.xpath('srccite/citeinfo/pubinfo/pubplace')[0].text
                self.citation.ui.fgdc_pubplace.setText(str(pubplace))
                publish = srcinfo.xpath('srccite/citeinfo/pubinfo/publish')[0].text
                self.citation.ui.fgdc_publish.setText(str(publish))
                # utils.populate_widget(self.citation.ui.fgdc_publish, srcinfo.xpath('srccite/citeinfo/pubinfo')[0])
            else:
                self.citation.ui.radio_pubinfoyes.setChecked(False)



            utils.populate_widget_element(self.ui.fgdc_srcscale, srcinfo, 'srcscale')

            typesrc = srcinfo.xpath('typesrc/text()')
            typesrc_text = str(typesrc[0])
            self.findChild(QComboBox, "fgdc_typesrc").setCurrentText(typesrc_text)

            utils.populate_widget_element(self.ui.fgdc_srccitea, srcinfo, 'srccitea')

            utils.populate_widget_element(self.ui.fgdc_srccontr, srcinfo, 'srccontr')


            # self.citation._from_xml(srccite.xpath('citeinfo')[0])

            if srcinfo.xpath('srctime'):
                timeperd = etree.Element('timeperd')
                timeinfo = srcinfo.xpath('srctime/timeinfo')[0]
                srccurr = srcinfo.xpath('srctime/srccurr')[0]
                srccurr.tag = 'current'
                # print srccurr
                timeperd.append(timeinfo)
                timeperd.append(srccurr)
                self.timeperd._from_xml(timeperd)
                # print timeperd
                #self.timeperd._from_xml(timeperd)



        except KeyError:
            pass


if __name__ == "__main__":
    utils.launch_widget(SRCInfo,
                        "SRCInfo testing")

