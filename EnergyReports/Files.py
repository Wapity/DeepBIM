#!/usr/bin/env python
# coding: utf-8
"""Extract revit files from success list and rename them with a counter to group them in the same folder"""

import os
PATH1 = "C://Users//Alex//DeepBIM"
PATH = "C://Users//Alex//DeepBIM//Data//00"
print(PATH)


with open(PATH1 + "//success.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]


files_paths = []
for i in range(len(content)):
    if content[i].endswith("ROOF ADDED"):
        files_paths.append(str(content[i][:-20]))


liste2 = []
for alpha in files_paths:
    liste2.append(alpha.replace('\\', '//'))


count = 0
for file_dir in liste2:
    a = os.listdir(path=file_dir)
    count += 1
    for file in a:
        if file.endswith(".rvt"):
            os.rename(file_dir + "//" + file, file_dir +
                      "//" + str(count) + ".rvt")
