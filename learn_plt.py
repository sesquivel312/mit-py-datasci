#!/usr/bin/env python
"""
tutorial links
    https://nbviewer.jupyter.org/github/matplotlib/AnatomyOfMatplotlib/blob/master/AnatomyOfMatplotlib-Part0-Intro2NumPy.ipynb
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from pprint import pprint as pp


pp(os.environ)

fig, ax = plt.subplots(nrows=2, ncols=2)
pp(type(fig))
pp(type(ax))
curr_ax = ax[0, 0]
curr_ax.plot([1,2,3,4], [1, 4, 2, 3], label='Line')
curr_ax.set(title='Plot title', ylabel='y-axis', xlabel='x-axis')
plt.legend()
plt.show()
