from pathlib import Path
import os
from sentence_extraction import tokenize_file
from aligning import main
from scrap_3 import populate_data
import sys

months = ['January','February','March','April','May','June','July','August','September','October','November','December']
year = sys.argv[1]
print(year)
for month in months[::-1]:
    path_scrap = os.getcwd()+"\\"+year+"\\"+month+"\\All\\"
    path_tokenize = os.getcwd()+"\\"+year+"\\"+month+"\\Tokenize\\"
    path_align = os.getcwd()+"\\"+year+"\\"+month+"\\Aligned\\"
    Path(path_scrap).mkdir(parents=True,exist_ok=True)
    print('populate_data(All,'+month+','+year+')')
    Path(path_tokenize).mkdir(parents=True,exist_ok=True)
    print('tokenize_file()')
