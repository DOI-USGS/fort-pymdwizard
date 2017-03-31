import requests

from dateutil import parser

from lxml import etree

from pymdwizard.core import xml_utils
from pymdwizard.core import utils


def validate_xml(xml, xsl_fname='fgdc', as_dataframe=False):
    """

    Parameters
    ----------
    xml : lxml document
                or
          filename
                or
          string containing xml representation

    xsl_fname : str (optional)
                can be one of:
                'fgdc' - uses the standard fgdc schema
                        ../resources/FGDC/fgdc-std-001-1998-annotated.xsd
                'bdp' = use the Biological Data profile schema,
                        ../resources/FGDC/BDPfgdc-std-001-1998-annotated.xsd
                full file path to another local schema.

                if not specified defaults to 'fgdc'

    Returns
    -------
        list of tuples
        (
    """

    if xsl_fname.lower() == 'fgdc':
        xsl_fname = utils.get_resource_path('fgdc/fgdc-std-001-1998-annotated.xsd')
    elif xsl_fname.lower() == 'bdp':
        xsl_fname = utils.get_resource_path('fgdc/BDPfgdc-std-001-1998-annotated.xsd')

    xmlschema_doc = etree.parse(xsl_fname)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_str = xml_utils.node_to_string(xml_utils.xml_document_loader(xml))
    tree = etree.ElementTree(etree.fromstring(xml_str))

    if xmlschema.validate(tree):
        return []

    # tree = etree.ElementTree(xml)
    line_lookup = dict([(e.sourceline, tree.getpath(e)) for e in tree.xpath('.//*')])
    line_lookup[tree.getroot().sourceline] = tree.getpath(tree.getroot())
    errors = []
    for error in xmlschema.error_log:
        try:
            errors.append((line_lookup[error.line][1:],
                           clean_error_message(error.message), error.line))
        except KeyError:
            errors.append(('Unknown', clean_error_message(error.message),
                           error.line))

    return errors


def clean_error_message(message):
    """
    Returns a cleaned up, more informative translation
    of a raw xml schema error message

    Parameters
    ----------
    message : str
              The raw message we will be cleaning up

    Returns
    -------
        str : cleaned up error message
    """
    parts = message.split()
    if 'Missing child element' in message:
        clean_message = "The {} is missing the expected element(s) '{}'".format(parts[1][:-1], parts[-2])
    elif r"The value '' is not accepted by the pattern '\s*\S(.|\n|\r)*'" in message or \
            "'' is not a valid value of the atomic type" in message:
        clean_message = "The value for {} cannot be empty".format(parts[1][:-1])
    else:
        clean_message = message
    return clean_message


def format_date(date_input):
    """

    Parameters
    ----------
    date_input : str or datetime
            if str provided must be in format that dateutil's parser can handle
    Returns
    -------
        str : date formated in FGDC YYYYMMDD format
    """

    if type(date_input) == str:
        date_input = parser.parse(date_input)

    return date_input.strftime('%Y%m%d')
