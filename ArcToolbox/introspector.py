import collections

import arcpy

def unique_values(fname, field):
    """
    return a list of the unique values in a single field

    Parameters
    ----------
    fname : str
            file name and path to the dataset that contains the field
    field : str
            name of field to examine

    Returns
    -------
    list
    """
    with arcpy.da.SearchCursor(fname, [field]) as cursor:
        return sorted({row[0] for row in cursor})


def get_min_max(fname, field):
    """
    returns the min and max values from a single field

    Parameters
    ----------
    fname : str
            file name and path to the dataset that contains the field
    field : str
            name of field to examine

    Returns
    -------
    tuple
    """
    min_value = arcpy.SearchCursor(fname, "", "", "", field + " A").next().getValue(field) #Get 1st row in ascending cursor sort
    max_value = arcpy.SearchCursor(fname, "", "", "", field + " D").next().getValue(field) #Get 1st row in descending cursor sort
    return min_value, max_value

def introspect_dataset(fname):
    fields = [f for f in arcpy.ListFields(fname)]
    results = collections.OrderedDict()
    for field in fields:
        field_name = field.name
        field_type = field.type
        print(field_name, field_type)
        if field_type in ['Integer', 'Single', 'SmallInteger', 'Double', 'Date']:
            contents = get_min_max(fname, field_name)
        elif field_type in ['OID', 'GlobalID']:
            contents = ["Internal feature number.",
                        "Sequential unique whole numbers that are automatically generated.",
                        "ESRI"]
        elif field_type in ['Guid']:
           contents = ['Globally Unique Identifier or GUID. ',
                       "Globally Unique Identifier or GUID. ",
                       "ESRI"]
        elif field_type == 'Geometry':
            contents = ['Feature geometry.',
                        'Coordinates defining the features.',
                        "ESRI"]

        elif field_type == 'String':
            contents = unique_values(fname, field_name)
        else:
            contents = ['',
                        '',
                        "Producer defined"]

        results[field_name] = {'type': field_type,
                               'contents':contents}
    return results