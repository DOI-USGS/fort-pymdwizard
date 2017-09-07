
import json

try:
    from habanero import cn
except ImportError:
    habanero = None

from pymdwizard.core.xml_utils import XMLNode

def clean_doi(doi):
    """
    Cleans doi to match expected string format.
    Removes leading 'https://'  and 'doi.org/' from the string

    Parameters
    ----------
    doi : str
        A string containing a DOI

    Returns
    -------
        DOI string with extraneous characters removed
    """
    if doi.startswith('https://doi.org/'):
        return doi.replace('https://doi.org/', '')
    elif doi.startswith('doi.org/'):
        return doi.replace('doi.org/', '')
    else:
        return doi


def get_doi_citation(doi):
    doi = clean_doi(doi)
    try:
        cite_data = json.loads(cn.content_negotiation(ids=doi, format = "citeproc-json"))
    except HTTPError:
        return None

    citeinfo = XMLNode(tag='citeinfo')
    for author in cite_data['author']:
        origin = XMLNode(tag='origin', parent_node=citeinfo, text=author['given'] + ' ' + author['family'])

    #
    if 'published-online' in cite_data:
        pubdate_parts = text=pubonline=cite_data['published-online']['date-parts'][0]
    elif 'published-print' in cite_data:
        pubdate_parts = text=pubonline=cite_data['published-print']['date-parts'][0]


    pubdate_str = ''.join(['{:02d}'.format(part) for part in pubdate_parts])
    pubdate = XMLNode(tag='pubdate', parent_node=citeinfo, text=pubdate_str)

    title = XMLNode(tag='title', parent_node=citeinfo, text=cite_data['title'])
    geoform = XMLNode(tag='geoform', parent_node=citeinfo, text='publication')
    serinfo = XMLNode(tag='serinfo', parent_node=citeinfo)
    sername = XMLNode(tag='sername', parent_node=citeinfo.serinfo, text=cite_data['container-title'])

    if 'volumne' in cite_data:
        issue_str = 'vol.' + ' ' + str(cite_data['volume']) + ', issue ' + cite_data['issue'] + ', ppg. ' + cite_data['page']
        issue = XMLNode(tag='issue', parent_node=citeinfo.serinfo, text=issue_str)
    if 'issue' in cite_data:
        issue_str = 'issue ' + cite_data['issue'] + ', ppg. ' + cite_data['page']
        issue = XMLNode(tag='issue', parent_node=citeinfo.serinfo, text=issue_str)

    pubinfo = XMLNode(tag='pubinfo', parent_node=citeinfo)
    pubplace = XMLNode(tag='pubplace', parent_node=citeinfo.pubinfo, text='n/a')
    publish = XMLNode(tag='publish', parent_node=citeinfo.pubinfo, text=cite_data['publisher'])
    onlink = XMLNode(tag='onlink', parent_node=citeinfo, text=cite_data['URL'])

    return citeinfo