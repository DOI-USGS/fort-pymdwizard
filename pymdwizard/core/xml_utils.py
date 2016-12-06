"""Various utility and misc functions used for manipulating XML

Attributes
----------

"""
# built in Python imports
import collections
import warnings

# external library imports
import lxml
try:
    import pandas as pd
except ImportError:
    warnings.warn('Pandas library not installed, dataframes disabled')
    pd = None


def node_to_dict(node):
    """

    Parameters
    ----------
    node : lxml element

    Returns
    -------
        dictionary contain a key value pair for each child item in the node
        where the key is the item's tag and the value is the item's text
    """
    node_dict = collections.OrderedDict()

    if len(node.getchildren()) == 0:
        tag = _parse_tag(node.tag)
        node_dict[tag] = node.text
    else:
        for child in node.getchildren():
            tag = _parse_tag(child.tag)
            if len(child.getchildren()) > 0:
                content = node_to_dict(child)
            else:
                content = child.text
            node_dict[tag] = content
    return node_dict


def _parse_tag(tag):
    """
    strips namespace declaration from xml tag string

    Parameters
    ----------
    tag : str

    Returns
    -------
    formatted tag

    """
    return tag[tag.find("}")+1:]


def element_to_list(results):
    """
    Returns the results(etree) formatted into a list of dictionaries.
    This is useful for flat data structures, e.g. homogeneous results that
    could be thought of and converted to a dataframe.

    Parameters
    ----------
    results : list of lxml nodes
        This list would could be returned from an xpath query for example

    Returns
    -------
    List of dictionaries. Each dictionary in this list is the result of
    the _node_to_dict function
    """
    return [node_to_dict(item) for item in results]


def element_to_df(results):
    """
    Returns the results (etree) formatted into a pandas dataframe.
    This only intended to be used on flat data structures, e.g. a list of
    homogeneous elements.
    For nested or hierarchical data structures this result will be awkward.

    Parameters
    ----------
    results : list of lxml nodes
        This list would could be returned from an xpath query for example

    Returns
    -------
    pandas dataframe
    """
    results_list = element_to_list(results)
    return pd.DataFrame.from_dict(results_list)


def elements_to_nested_dict(results):
    """
    Returns the results (etree) formatted into a nested dictionary.
    This is intended to be used hierarchical data structures.

    Parameters
    ----------
    results : list of lxml nodes
        This list would could be returned from an xpath query for example

    Returns
    -------
    pandas dataframe
    """
    return node_to_dict(results)
