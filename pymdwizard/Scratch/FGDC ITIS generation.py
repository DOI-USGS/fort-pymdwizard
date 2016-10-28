
# coding: utf-8

# # How to make a FGDC taxonomy in python

# ### Step 1 use ITIS to get a list of species identiviers (TSNs) 
# pytaxize makes this easy

# In[1]:

import pytaxize


# In[ ]:

#species to include: Grizzly bear, bald eagle, ladybug, raccoon
species = []


# ## Start with a search of the common names to find the appropriate taxonomic serial numbers (tsns)

# In[2]:

pytaxize.itis.searchbycommonname('grizzly bear')


# In[3]:

pytaxize.itis.searchbycommonname('bald eagle')


# In[7]:

pytaxize.itis.searchbycommonname('ladybird')


# In[8]:

pytaxize.itis.searchbycommonname('raccoon')


# ### Make a list of the final ones to include in our taxonomy

# In[9]:

tsns = [180543, 175420, 114329, 180575]


# ### for each of these we can query ITIS to get the full heirarchy  as a list of elements:

# In[10]:

pytaxize.itis.getfullhierarchyfromtsn(180575)


# In[12]:

results = []
for tsn in tsns:
    heirarchy = pytaxize.itis.getfullhierarchyfromtsn(tsn)
    heirarchy = [r for r in heirarchy if r['parentTsn'] != str(tsn)]
    results.append(heirarchy)


# ## But to make these easier to work with for merging and traversing the heirarchy let's implement an object oriented abstraction of the data structure. (this prototype will get incorporated into a TBD package when finalized)

# In[11]:

class taxon(object):
    def __init__(self, rankname, taxonname, 
                 tsn, children=None, parent=None):
        self.rankname = rankname
        self.taxonname = taxonname
        self.tsn = tsn
        if children:
            self.children = children
        else:
            self.children = []
        self.parent = parent
        self.indent = "  "*int(int(indent_lookup[rankname])/10)
    
    def __eq__(self, other):
        return self.rankname == other.rankname and self.taxonname == other.taxonname and self.tsn == other.tsn
    
    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        string = self.indent+"{}:{} (tsn={})\n".format(self.rankname, self.taxonname, self.tsn)
        if self.children:
            string += "".join([str(c) for c in self.children])
        return string
    
    def add_child(self, child):
        child.parent = self
#         child.indent = "  "+self.indent
        self.children.append(child)
        
    def find_child_by_tsn(self, tsn):
        if self.tsn == tsn:
            return self
        else:
            for child in self.children:
                match = child.find_child_by_tsn(tsn)
                if match:
                    return match
        return None
                    
    
    
        


# ### Some more code for cycling through our list of species and merging them in a complete taxonomy tree

# In[13]:

ranknames = pytaxize.itis.getranknames()
del ranknames['kingdomname']
ranknames.drop_duplicates(inplace=True)
ranknames.set_index('rankname', inplace=True)

indent_lookup = ranknames.to_dict()['rankid']
indent_lookup['Life'] = 0

life = taxon(rankname="Life", taxonname='Life', tsn=None)
for heirarchy in results:
    for taxonomy in heirarchy:
        #see if taxonomy is alreay there
        existing_taxon = life.find_child_by_tsn(taxonomy['tsn'])
        if not existing_taxon:
            child_taxon = taxon(rankname=taxonomy['rankName'],
                                taxonname=taxonomy['taxonName'],
                                tsn=taxonomy['tsn'])

            parent = life.find_child_by_tsn(taxonomy['parentTsn'])
            parent.add_child(child_taxon)


# In[19]:

#notice the use of a __str__ and __repr__ method to provide a handy printout of our taxonomic tree!
print(life)


# # Now we just need to convert this to fgdc xml 

# In[34]:

c.tsn
df = pytaxize.itis.getcommonnamesfromtsn(c.tsn)
df.query('lang =="English"').comname.iloc[0]


# In[35]:

from lxml import etree

def gen_taxclass(taxon, include_common_names=False):
    taxonomicclassification = etree.Element("taxoncl")
    taxrankname = etree.Element("taxonrn")
    taxrankname.text = taxon.rankname
    taxonomicclassification.append(taxrankname)

    taxrankvalue = etree.Element("taxonrv")
    taxrankvalue.text = taxon.taxonname
    taxonomicclassification.append(taxrankvalue)
    
    if include_common_names and taxon.tsn:
        df = pytaxize.itis.getcommonnamesfromtsn(taxon.tsn)
        common_name = df.query('lang =="English"').comname.iloc[0]
        applicable_common_name = etree.Element("common")
        applicable_common_name.text = common_name
        taxonomicclassification.append(applicable_common_name)
        
    for child in taxon.children:
        child_node = gen_taxclass(child, include_common_names)
        taxonomicclassification.append(child_node)
        
    return taxonomicclassification


# In[37]:

taxonomic_taxclass = gen_taxclass(root)


# In[43]:

print(etree.tostring(taxonomic_taxclass, pretty_print=True).decode())

