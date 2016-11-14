
# coding: utf-8

# # How to make a FGDC taxonomy section using pymdwizard

# # (TODO: make a GUI which provides this functionality to a general audience)

# ### Step 1 use ITIS to get a list of species identifiers (TSNs) 

# In[1]:

import sys
sys.path.insert(0, r'N:\Metadata\MetadataWizard\pymdwizard')

from pymdwizard.core import taxonomy


# In[2]:

taxonomy.search_by_common_name('whitebark pine')


# In[3]:

taxonomy.search_by_common_name('pine beetle', as_dataframe=True)


# In[4]:

taxonomy.search_by_common_name('blister rust')


# In[5]:

taxonomy.search_by_scientific_name("gulo gulo")


# ## From the queries above we need to make a list of the exact tsns to include

# In[6]:

tsns = [183311, 114918, 192053, 179750, 180551]


# # This hierarchy can be converted into FGDC format with the 'gen_fgdc_taxonomy' function

# In[7]:

fgdc_taxonomy = taxonomy.gen_fgdc_taxonomy(tsns, include_common_names=True)

#lxml is being imported just so that we can print out this node in the notebook
from lxml import etree
print(etree.tostring(fgdc_taxonomy, pretty_print=True).decode())


# In[8]:

taxonomic_hierarchy = taxonomy.merge_taxons(tsns)
taxonomic_hierarchy


# # This hierarchy can be converted into FGDC format with the 'gen_fgdc_taxonomy' function

# In[9]:

from lxml import etree
fgdc_taxonomy = taxonomy.gen_fgdc_taxonomy(tsns, include_common_names=True)

print(etree.tostring(fgdc_taxonomy, pretty_print=True).decode())


# In[ ]:



