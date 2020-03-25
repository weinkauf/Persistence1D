import matplotlib.pyplot as plt
import numpy as np
from persistence1d import RunPersistence

"""
The file exemplifies different use cases for Persistence1D:

* Loading data from file
* Generating data in memory
* Running Persistence1D to obtain minima/maxima and their persistence
* Filtering minima/maxima by their persistence
* Printing the (filtered) list of minima/maxima
* Visualizing the (filtered) list of minima/maxima together with the input data

"""

def LoadData(Filename):
    #~ Input Data comes from a file. In our case, it is a list of numbers (floats) with one number per line.
    InputData = np.genfromtxt(Filename, delimiter=',', dtype=None)
    return InputData


def GenerateData():
    #~ Generate data using sine function and different frequencies.
    x = np.arange(600.0)
    SineLowFreq = np.sin(x * 0.01 * np.pi)
    SineMedFreq = 0.25 * np.sin(x * 0.01 * np.pi * 4.9)
    SineHighFreq = 0.15 * np.sin(x * 0.01 * np.pi * 12.1)
    InputData = SineLowFreq + SineMedFreq + SineHighFreq
    return InputData
    

def SetData():
    #~ Set the data directly in code
    InputData = np.array([2.0, 5.0, 7.0, -12.0, -13.0, -7.0, 10.0, 18.0, 6.0, 8.0, 7.0, 4.0])
    return InputData


def FilterExtremaByPersistence(ExtremaAndPersistence, Threshhold):
    FilteredExtremaAndPersistence = [t for t in ExtremaAndPersistence if t[1] > Threshhold]
    return FilteredExtremaAndPersistence


def SortExtremaByPersistence(ExtremaAndPersistence):
    #~ Sort the list of extrema by persistence.
    #~ The original list from RunPersistence() is not guaranteed to be sorted,
    #~ although it may appear sorted in many cases.
    #~ This call to sorted() creates a new list. If you want to sort in-place, use ExtremaAndPersistence.sort()
    SortedExtremaAndPersistence = sorted(ExtremaAndPersistence, key=lambda ExtremumAndPersistence: ExtremumAndPersistence[1])
    return SortedExtremaAndPersistence


def PrintExtrema(InputData, ExtremaAndPersistence):
    for i, E in enumerate(ExtremaAndPersistence):
        strType = "Minimum" if (i % 2 == 0) else "Maximum"
        print("%s at index %d with persistence %g and data value %g" % (strType, E[0], E[1], InputData[E[0]]))


def ComputeExtremaAndPersistence(InputData):
    #~ This simple call is all you need to compute the extrema of the given data and their persistence.
    ExtremaAndPersistence = RunPersistence(InputData)
    return ExtremaAndPersistence


def Visualize(InputData, ExtremaAndPersistence):
    #~ Define colors and other style choices
    LineStyle = dict(color=(0.0, 0., 0.))
    MarkerStyleMinima = dict(linestyle='', markersize=10, color=(0.3, 0.3, 1.0))
    MarkerStyleMaxima = dict(linestyle='', markersize=10, color=(1.0, 0.2, 0.2))
    MarkerStyleGlobalMin = dict(linestyle='', markersize=11, color=(0.0, 0.0, 1.0))

    #~ Create Plot
    fig, ax = plt.subplots()
    
    #~ Plot the original data as a line plot
    ax.plot(range(0, len(InputData)), InputData, **LineStyle)

    #~ Get the indices of the minima and maxima as well as the global minimum
    Minima = [t[0] for t in ExtremaAndPersistence[::2]]
    Maxima = [t[0] for t in ExtremaAndPersistence[1::2]]
    GlobalMin = Minima[-1]
    Minima = Minima[:-2] #remove the global minimum from the list of minima, so we do not plot it twice

    #~ Plot the minima and maxima as well as the global minimum
    ax.plot(Minima, InputData[Minima], marker='.', **MarkerStyleMinima)
    ax.plot(Maxima, InputData[Maxima], marker='.', **MarkerStyleMaxima)
    ax.plot(GlobalMin, InputData[GlobalMin], marker='.', **MarkerStyleGlobalMin)

    #~ Set some labels and grid
    ax.set(xlabel='data index', ylabel='data value')
    ax.set_aspect(1.0/ax.get_data_ratio()*0.2)    
    ax.grid()

    #~ Save picture as PNG and show the interactive window
    fig.savefig("MatplotlibVisRes.png")
    plt.show()


#~ Example 1: Generate some data using sine functions, extract and filter the extrema, show them
print("Example 1:")
InputData = GenerateData()
ExtremaAndPersistence = ComputeExtremaAndPersistence(InputData)
ExtremaAndPersistence = FilterExtremaByPersistence(ExtremaAndPersistence, 0.5) #try commenting out this line
PrintExtrema(InputData, ExtremaAndPersistence)
Visualize(InputData, ExtremaAndPersistence)

#~ Example 2: Load data, extract, sort, filter the extrema, and print them to console
print("\nExample 2:")
InputData = LoadData("data.txt")
ExtremaAndPersistence = ComputeExtremaAndPersistence(InputData)
ExtremaAndPersistence = SortExtremaByPersistence(ExtremaAndPersistence) #try commenting out this line
#~ ExtremaAndPersistence = FilterExtremaByPersistence(ExtremaAndPersistence, 10) #try commenting out this line
PrintExtrema(InputData, ExtremaAndPersistence)

#~ Example 3: Set data in code, extract the extrema, and print them to console
print("\nExample 3:")
InputData = SetData()
PrintExtrema(InputData, ComputeExtremaAndPersistence(InputData))
