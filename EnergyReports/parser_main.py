import csv
import os
import pandas as pd

from html_extractor import html_single_extractor

""" Extactor of heating/cooling load and parameters for all buildings from Htm folder
of .htm Revit 'standard' reports """

"""OPENING"""
PATH = "/Users/alex/Desktop/ArchiBIM/DeepBIM/EnergyReports/Htm"  # change to location of htm reports of Revit
get_keys = True

with open('bim_train.csv', mode='w') as bim_train:
    bim_writer = csv.writer(bim_train, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for file in os.listdir(PATH):
        if file.endswith(".htm"):
            with open(os.path.join(PATH, file), "r", encoding='utf-16') as f:
                raw_text = f.read()
            text = raw_text.split()

            if get_keys:
                keys, items = html_single_extractor(text, get_keys)
                # print(keys)
                bim_writer.writerow(keys)
            else:
                items = html_single_extractor(text, get_keys)

            bim_writer.writerow(items)
            get_keys = False

# reader = pd.read_csv('bim_train.csv')
# print(reader)
