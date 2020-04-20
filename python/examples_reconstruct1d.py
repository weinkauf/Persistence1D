import numpy as np
from persistence1d import RunPersistence
from reconstruct1d import RunReconstruction
from examples_visualize import Visualize

"""
The file exemplifies different use cases for Reconstruct1D:

* Loading data from file
* Generating data in memory with different shapes and noise
* Running Persistence1D to obtain minima/maxima and their persistence
* Filtering minima/maxima by their persistence
* Running Reconstruct1D with the filtered set of extrema to obtain a smoothed version of the input data.
   Notably, this new data contains only the filtered minima/maxima.
* Creating a smooth function using user-defined minima/maxima and data values.
* Influence of the biharmonic or triharmonic smoothing setting
* Influence of the Data Weight parameter
* Increasing the output's resolution to obtain smoother results
* Visualizing the (filtered) list of minima/maxima together with the input/smoothed data
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


def GenerateDataConvexConcave(Sigma = 0.025):
    p = 8
    n = 50
    x = np.arange(n+1)
    Left = np.power(x/n, p)
    Right = (1 - Left)[1:]
    NoNoise = np.concatenate((Left, Right, Left[1:], Right, Left[1:], Right))
    np.random.seed(111)
    InputData = NoNoise + np.random.normal(0, Sigma, len(NoNoise))
    return InputData
    

def SetData():
    #~ Set the data directly in code
    InputData = np.array([2.0, 5.0, 7.0, -12.0, -13.0, -7.0, 10.0, 18.0, 6.0, 8.0, 7.0, 4.0])
    return InputData


def IncreaseDataResolution(InputData, SuperSample):
    #~ Increase resolution by straightforward linear interpolation between original samples.
    #~ This yields the same topology. The smoothed output will be smoother.
    if (SuperSample > 1):
        from scipy.interpolate import interp1d
        x = np.linspace(0, len(InputData)-1, num = len(InputData), endpoint=True)
        f = interp1d(x, InputData)
        xnew = np.linspace(0, len(InputData)-1, num = len(InputData) + SuperSample*(len(InputData)-1), endpoint=True)
        InputData = f(xnew)
    return InputData


def FilterExtremaByPersistence(ExtremaAndPersistence, Threshhold):
    FilteredExtremaAndPersistence = [t for t in ExtremaAndPersistence if t[1] > Threshhold]
    return FilteredExtremaAndPersistence


def ComputeExtremaAndPersistence(InputData):
    #~ This simple call is all you need to compute the extrema of the given data and their persistence.
    ExtremaAndPersistence = RunPersistence(InputData)
    return ExtremaAndPersistence


if __name__== "__main__":

    #~ Example 1: Generate some data using sine functions, extract and filter the extrema, reconstruct a smoothed version of the data with fewer extrema, plot that on top of the original data
    print("Example 1:")
    InputData = GenerateData()
    Extrema = ComputeExtremaAndPersistence(InputData)
    FigAx = Visualize(InputData, Extrema, None, 'data extrema dotted', DataLabel="Original Data")
    Extrema = FilterExtremaByPersistence(Extrema, 0.5) #try commenting out this line or changing the threshhold
    SmoothData = RunReconstruction(InputData, [t[0] for t in Extrema], 'biharmonic', 0.0000001)
    Visualize(SmoothData, Extrema, FigAx, 'extrema data fat', DataLabel="Smoothed Data", SaveFilename="Reconstruct1D_Example1.png")

    #~ Example 2: Generate some data using sine functions, extract and filter the extrema, manually delete some extrema, reconstruct a smoothed version of the data with fewer extrema, plot that on top of the original data
    print("Example 2:")
    InputData = GenerateData()
    Extrema = ComputeExtremaAndPersistence(InputData)
    FigAx = Visualize(InputData, Extrema, None, 'data extrema dotted', DataLabel="Original Data")
    Extrema = FilterExtremaByPersistence(Extrema, 0.5) #try commenting out this line or changing the threshhold
    #~ Manually remove the second minimum/maximum pair.
    #~ Careful, you need to have a monotonically alternating sequence afterwards: min, max, min, max, min
    #~ If you remove arbitrarily, the results may be topologically incorrect and/or a solution may not be found.
    del Extrema[2:4]
    #~ Extrema = [Extrema[-1]] #Keep only the global minimum
    SmoothData = RunReconstruction(InputData, [t[0] for t in Extrema], 'biharmonic', 0.0000001)
    Visualize(SmoothData, Extrema, FigAx, 'extrema data fat', DataLabel="Smoothed Data", SaveFilename="Reconstruct1D_Example2.png")

    #~ Example 3: We design a set of extrema and prescribe data values for them, but for no other point.
    #~ Then we apply a purely biharmonic and triharmonic reconstruction without data weight.
    #~ This highlights the difference between a C1 and a C2 curve nicely.
    #~ This also shows how to create data with topological constraints from scratch.
    print("Example 3:")
    InputData = np.arange(600.0)
    #~ Design the locations of the extrema. Persistence is zero for all of them, since we will not filter anyway
    DesignedExtrema = [(100, 0), (300, 0), (400, 0), (440, 0), (500, 0)]
    #~ Design the data values for the extrema.
    #~ You need to have a monotonically alternating sequence afterwards, starting and ending with minima: min, max, min, max, min
    InputData[100] = -1
    InputData[300] = 1
    InputData[400] = -1
    InputData[440] = 1
    InputData[500] = -1
    #~ The first and last point need to be constrained to proper values as well. The optimization step uses these values.
    #~ When looking at the function, you may consider these points as maxima, but topologically we do not.
    #~ If you end up having these points lower than their direct neighbors, then they become proper minima and you need to include them in the above alternating sequence instead of here.
    InputData[  0] = 0
    InputData[599] = 0
    SmoothDataBiharmonic = RunReconstruction(InputData, [t[0] for t in DesignedExtrema], 'biharmonic', 0)
    FigAx = Visualize(SmoothDataBiharmonic, DesignedExtrema, None, 'data fat solid', DataLabel="Biharmonic Reconstruction")
    SmoothDataTriharmonic = RunReconstruction(InputData, [t[0] for t in DesignedExtrema], 'triharmonic', 0)
    Visualize(SmoothDataTriharmonic, DesignedExtrema, FigAx, 'extrema data fat dashed', DataLabel="Triharmonic Reconstruction", SaveFilename="Reconstruct1D_Example3.png")

    #~ Example 4: Generate noisy data with convex and concave shapes, extract and filter the extrema, reconstruct a smoothed version of the data with fewer extrema, plot that on top of the original data.
    #~ Shows how the smooth reconstruction tries to adapt to the data depending on the data weight parameter.
    print("Example 4:")
    InputData = GenerateDataConvexConcave(0.025)
    Extrema = ComputeExtremaAndPersistence(InputData)
    Filtered = FilterExtremaByPersistence(Extrema, 0.5) #try changing the threshhold
    for (i, DataWeight) in enumerate([0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1]): #try other values for the data weight
        SmoothData = RunReconstruction(InputData, [t[0] for t in Filtered], 'biharmonic', DataWeight)
        FigAx = Visualize(InputData, Extrema, None, 'data thin', DataLabel="Original Data")
        Visualize(SmoothData, Filtered, FigAx, 'extrema data fat', DataLabel="Smoothed Data with Data Weight %g" % DataWeight, SaveFilename="Reconstruct1D_Example4_%d.png" % i)

    #~ Example 5: Generate low-res data, extract and filter the extrema, reconstruct a smoothed, high-res version of the data, plot that on top of the original data.
    print("Example 5:")
    #~ InputData = LoadData('data.txt') #try also loading from file
    InputData = SetData()
    InputData = IncreaseDataResolution(InputData, 50) #try commenting out this line or changing the supersampling factor
    Extrema = ComputeExtremaAndPersistence(InputData)
    FigAx = Visualize(InputData, Extrema, None, 'data extrema dotted', DataLabel="Original Data")
    Extrema = FilterExtremaByPersistence(Extrema, 10) #try commenting out this line or changing the threshhold
    SmoothData = RunReconstruction(InputData, [t[0] for t in Extrema], 'biharmonic', 0.0000001)
    Visualize(SmoothData, Extrema, FigAx, 'extrema data fat', DataLabel="Smoothed Data", SaveFilename="Reconstruct1D_Example5.png")

    #~ Example 6: An animation with varying persistence thresholds: Generate some data using sine functions, extract and filter the extrema, reconstruct a smoothed version of the data with fewer extrema, plot it.
    print("Example 6:")
    InputData = GenerateData()
    Extrema = ComputeExtremaAndPersistence(InputData)
    for (i, PersistenceThreshold) in enumerate([0, 0.1, 0.2, 0.3, 0.4, 0.5]):
        Filtered = FilterExtremaByPersistence(Extrema, PersistenceThreshold)
        SmoothData = RunReconstruction(InputData, [t[0] for t in Filtered], 'biharmonic', 0)
        Visualize(SmoothData, Filtered, None, 'extrema data fat', DataLabel="Smoothed Data with Persistence Threshold %g" % PersistenceThreshold, SaveFilename="Reconstruct1D_Example6_%d.png" % i)


    #~ The plot results can be cropped using ImageMagick like this:
    #~ magick mogrify -trim -identify Reconstruct1D_Example*
    
    #~ Example 4 can be made into an animated GIF using this ImageMagick command line:
    #~ magick -delay 100 Reconstruct1D_Example4_* -trim +repage -layers optimize -identify reconstruct1d_example4.gif

    #~ Example 6 can be made into an animated GIF using this ImageMagick command line:
    #~ magick -delay 100 Reconstruct1D_Example6_* Reconstruct1D_Example6_5.png -trim +repage -layers optimize -identify reconstruct1d_example6.gif