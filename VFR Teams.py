
# coding: utf-8

# In[1]:

import numpy as np
from datascience import *
import matplotlib
import matplotlib.pyplot as plots


# In[23]:

VFR=Table.read_table("VFR-Master-Data.csv")


# In[25]:

Differences=VFR.drop(0,1,2,3,4,6,7,8).group("Team",np.average)


# In[26]:

print(Differences)



