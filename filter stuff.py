# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.signal as signal
# import data
filename = "C:\\Users\\jnewk\\Documents\\MATLAB\\Filters\\2016.03.23 CDM files\\dat10.csv"
dat = pd.read_csv(filename)
samplerate = 1000/np.mean(np.diff(dat['time']))
time = np.array(dat['time'])
y = np.array(dat['kPa'])
CFC = 60
freq = CFC*5/3
Wn=100/samplerate*2
l_pad = np.int(0.01*samplerate)
l_pad = min(max(l_pad,100),len(y)-1)

b, a = signal.butter(2,Wn,'low')
y2 = signal.filtfilt(b, a, y,padtype = 'odd', padlen = l_pad)

plt.hold(True)
plt.plot(time,y)
plt.plot(time,y2,'-r')
edapt = pd.read_csv("C:\\Users\\jnewk\\Documents\\MATLAB\\Filters\\2016.03.23 CDM files\\edapt.csv")
y_e = np.array(edapt['kPa'])
plt.plot(time,y_e,'-g')
diff_Edapt = y_e - y2
max(diff_Edapt)