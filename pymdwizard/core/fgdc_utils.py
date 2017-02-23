import requests

from dateutil import parser

from lxml import etree
from lxml import html

from pymdwizard.core import xml_utils

def validate_xml(xml, xsl_fname):

    xmlschema_doc = etree.parse(xsl_fname)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    # tree = etree.ElementTree(xml)
    tree =  etree.ElementTree(etree.fromstring(xml_utils.node_to_string(xml)))

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
