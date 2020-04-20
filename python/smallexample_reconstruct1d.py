import matplotlib.pyplot as plt
import numpy as np
from persistence1d import RunPersistence
from reconstruct1d import RunReconstruction

#~ Generate data using sine function and different frequencies.
x = np.arange(600.0)
SineLowFreq = np.sin(x * 0.01 * np.pi)
SineMedFreq = 0.25 * np.sin(x * 0.01 * np.pi * 4.9)
SineHighFreq = 0.15 * np.sin(x * 0.01 * np.pi * 12.1)
InputData = SineLowFreq + SineMedFreq + SineHighFreq

#~ Compute the extrema of the given data and their persistence.
ExtremaAndPersistence = RunPersistence(InputData)

#~ Keep only those extrema with a persistence larger than 0.5.
FilteredIndices = [t[0] for t in ExtremaAndPersistence if t[1] > 0.5]

#~ This simple call is all you need to reconstruct a smooth function containing only the filtered extrema
SmoothData = RunReconstruction(InputData, FilteredIndices, 'biharmonic', 0.0000001)

#~ Plot original and smoothed data
fig, ax = plt.subplots()
ax.plot(range(0, len(InputData)), InputData, label="Original Data")
ax.plot(range(0, len(SmoothData)), SmoothData, label="Smooth Data")
ExtremaIndices = [t[0] for t in ExtremaAndPersistence]
ax.plot(ExtremaIndices, InputData[ExtremaIndices], marker='.', linestyle='')
ax.plot(FilteredIndices, InputData[FilteredIndices], marker='*', linestyle='')
ax.set(xlabel='data index', ylabel='data value')
ax.set_aspect(1.0/ax.get_data_ratio()*0.2)    
ax.grid()
plt.legend()    
plt.show()
