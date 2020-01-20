#!/usr/bin/env python
# coding: utf-8

# In[34]:


import os 
PATH1 = "C://Users//Alex//DeepBIM" 
PATH = "C://Users//Alex//DeepBIM//Data//00" 
print(PATH)


# In[62]:


with open(PATH1 + "//success.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content] 


# In[36]:


files_paths = []
for i in range(len(content)):
    if content[i].endswith("ROOF ADDED") : 
        files_paths.append(str(content[i][:-20]))


# In[52]:


liste2 = []
for alpha in files_paths:
    liste2.append(alpha.replace('\\', '//'))


# In[61]:


count =0
for file_dir in liste2:
    a = os.listdir(path=file_dir)
    count+=1
    for file in a:
        if file.endswith(".rvt"):
            os.rename(file_dir+ "//" + file, file_dir + "//" + str(count) + ".rvt")

