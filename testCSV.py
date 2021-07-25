import pandas as pd
import numpy as np
import community
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy
import time
import os
import csv
import codecs

loop_file = codecs.open('./loop.csv','w+','utf-8')
loop_writer = csv.writer(loop_file,delimiter=',',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
loop_writer.writerow([1, 3, 3])
loop_file.close()
