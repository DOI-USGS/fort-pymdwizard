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
Module contains functionality for creating a metadata review document.


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
import time
import getpass

try:
    from docx import Document
    from docx.shared import Inches
    from docx.shared import Pt
    from docx.shared import RGBColor
    from docx.enum.style import WD_STYLE_TYPE
except ImportError:
    docx = None

from pymdwizard.core import utils
from pymdwizard.core import fgdc_utils

FGDC_LOOKUP = fgdc_utils.get_fgdc_lookup()


def _get_longname(tag):
    try:
        long_name = FGDC_LOOKUP[tag]['long_name']
    except KeyError:
        long_name = tag

    return long_name


def _load_styles(doc):
    heading1 = doc.styles['Normal']
    font = heading1.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(24)
    font.bold = True

    styles = doc.styles
    new_heading_style = styles.add_style('fgdc title', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Heading 1']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(24)
    font.bold = True

    new_heading_style = styles.add_style('fgdc heading 2', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Heading 2']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(18)
    font.bold = True

    new_heading_style = styles.add_style('fgdc heading 3', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Heading 3']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(13.5)
    font.bold = True

    new_heading_style = styles.add_style('review content heading', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Heading 3']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x36, 0x5F, 0x91)
    font.size = Pt(13.5)
    font.bold = True

    new_heading_style = styles.add_style('fgdc bar', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Normal']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    font.size = Pt(12)
    font.bold = True

    new_heading_style = styles.add_style('fgdc tag', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Normal']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x48, 0x8A, 0xC7)
    font.size = Pt(12)
    font.italic = True

    new_heading_style = styles.add_style('fgdc tag content', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Normal']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x15, 0x15, 0x15)
    font.size = Pt(12)
    font.italic = False
    font.bold = False

    new_heading_style = styles.add_style('fgdc bold', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Normal']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x15, 0x15, 0x15)
    font.size = Pt(12)
    font.italic = False
    font.bold = True

    new_heading_style = styles.add_style('fgdc link', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['List Bullet']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0xFF)
    font.size = Pt(12)
    font.underline = True
    font.bold = False


def _add_tag(doc, tag, content='', indent=0,
             tag_style='fgdc tag', content_style='fgdc tag content'):
    cit = doc.add_paragraph(tag + ': ', style=tag_style)
    cit.paragraph_format.space_after = Inches(.005)
    if content:
        if len(content) > 70:
            content = doc.add_paragraph(content, style=content_style)
            content.paragraph_format.left_indent = Inches(indent)
            content.paragraph_format.line_spacing = 1
        else:
            content = cit.add_run(content)
            content.italic = False
            content.bold = False
            content.font.color.rgb = RGBColor(0x15, 0x15, 0x15)

    return cit


def _add_child_content(doc, node, indent=0.25):
    line = _add_tag(doc, _get_longname(node.tag), node.text, indent)
    line.paragraph_format.left_indent = Inches(indent)
    for child in node.children:
        _add_child_content(doc, child, indent+0.25)


def format_errors(xml_document, which='bdp'):

    if which == 'bdp':
        xsl_fname = utils.get_resource_path('FGDC/BDPfgdc-std-001-1998-annotated.xsd')
    else:
        xsl_fname = utils.get_resource_path('FGDC/fgdc-std-001-1998-annotated.xsd')

    return fgdc_utils.validate_xml(xml_document.record, xsl_fname)


def generate_review_report(xml_document, docx_fname, which='bdp'):

    document = Document()

    DOCX = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    element = document.settings.element.find(DOCX + 'proofState')
    element.attrib[DOCX + 'grammar'] = 'dirty'
    element.attrib[DOCX + 'spelling'] = 'dirty'

    _load_styles(document)

    title_str = "Metadata Review for:\n\t{}"
    try:
        title_str = xml_document.metadata.idinfo.citation.citeinfo.title.text
    except:
        title_str = "No FGDC Title found in record at metadta/idinfo/citation/citeinfo/title"

    title = document.add_heading("Metadata Review for:", level=2)
    title.style = document.styles['fgdc heading 2']
    title.paragraph_format.line_spacing = 1
    title2 = document.add_paragraph("\t"+title_str+'\n',
                                    style='fgdc tag content')
    bar = title2.add_run('_'*72)
    document.add_paragraph('')

    reviewinfoline = document.add_heading('Review Info:', level=3)
    reviewinfoline.style = document.styles['review content heading']
    fname = os.path.split(xml_document.fname)[-1]
    _add_tag(document, "Metadata file being reviewed", fname,
             tag_style='fgdc bold')
    try:
        username = getpass.getuser()
        contact = utils.get_usgs_contact_info(username, True)
        reviewer_str = "{} ({})".format(contact['fgdc_cntperp']['fgdc_cntper'],
                                        contact['fgdc_cntemail'])
    except:
        # something when wrong getting the contact info
        # (no internet, non USGS, etc), just insert placeholcers
        reviewer_str ="<<insert reviewer name>> (<<insert reviewer email>>)"

    _add_tag(document, "Reviewer", reviewer_str,
             tag_style='fgdc bold')
    _add_tag(document, "Review Date", time.strftime("%m/%d/%Y"),
             tag_style='fgdc bold')
    document.add_paragraph('')

    summaryline = document.add_heading('Summary:', level=3)
    summaryline.style = document.styles['review content heading']
    document.add_paragraph('<<insert general review comments here>>', style='fgdc tag content')
    document.add_paragraph('', style='fgdc tag content')
    document.add_paragraph('', style='fgdc tag content')

    errorline = document.add_heading('FGDC Schema Errors:', level=3)
    errorline.style = document.styles['review content heading']

    errors = format_errors(xml_document, which)
    if errors:
        document.add_paragraph('Error (XML Path to error)', style='fgdc tag')
        for error in errors:
            e = document.add_paragraph('\t{}\n\t({})'.format(error[1], error[0]),
                                   style='fgdc tag content')
    else:
        document.add_paragraph('\tNo Schema Errors found', style='fgdc tag')

    document.add_paragraph('')

    mdcontentline = document.add_heading('Metadata Content:', level=3)
    mdcontentline.style = document.styles['review content heading']
    bar = document.add_paragraph('_'*72, style='fgdc bar')
    title2 = document.add_heading('Metadata:', level=3)
    title2.style = document.styles['fgdc heading 3']

    for child in xml_document.metadata.children:
        long_name = _get_longname(child.tag)
        link = document.add_paragraph(text=long_name, style='fgdc link')
        link.paragraph_format.left_indent = Inches(0.5)
        link.paragraph_format.line_spacing=1

    for child in xml_document.metadata.children:
        long_name = _get_longname(child.tag)
        bar = document.add_paragraph('_'*72, style='fgdc bar')

        section_title = document.add_heading(long_name+ ':', level=3)
        section_title.style = document.styles['fgdc heading 3']
        section_title.paragraph_format.space_after = Inches(.15)
        _add_child_content(document, child)

    document.save(docx_fname)
