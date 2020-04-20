from unionfind import UnionFind
import numpy as np


def RunPersistence(InputData):
    """
    Finds extrema and their persistence in one-dimensional data.
    
    Local minima and local maxima are extracted, paired,
    and returned together with their persistence.
    The global minimum is extracted as well.

    We assume a connected one-dimensional domain.
    Think of "data on a line", or a function f(x) over some domain xmin <= x <= xmax.
    We are only concerned with the data values f(x)
    and do not care to know the x positions of these values,
    since this would not change which point is a minimum or maximum.
    
    This function returns a list of extrema together with their persistence.
    The list is NOT sorted, but the paired extrema can be identified, i.e.,
    which minimum and maximum were removed together at a particular
    persistence level. As follows:
    The odd entries are minima, the even entries are maxima.
    The minimum at 2*i is paired with the maximum at 2*i+1.
    The last entry of the list is the global minimum.
    It is not paired with a maximum.
    Hence, the list has an odd number of entries.
    
    Author: Tino Weinkauf
    """
 
    #~ How many items do we have?
    NumElements = len(InputData)
    
    #~ Sort data in a stable manner to break ties (leftmost index comes first)
    SortedIdx = np.argsort(InputData, kind='stable')

    #~ Get a union find data structure
    UF = UnionFind(NumElements)

    #~ Paired extrema
    ExtremaAndPersistence = []

    #~ Watershed
    for idx in SortedIdx:
        
        #~ Get neighborhood indices
        LeftIdx = max(idx - 1, 0)
        RightIdx = min(idx + 1, NumElements - 1)
        
        #~ Count number of components in neighborhhood
        NeighborComponents = []
        LeftNeighborComponent = UF.Find(LeftIdx)
        RightNeighborComponent = UF.Find(RightIdx)
        if (LeftNeighborComponent != UnionFind.NOSET): NeighborComponents.append(LeftNeighborComponent)
        if (RightNeighborComponent != UnionFind.NOSET): NeighborComponents.append(RightNeighborComponent)
        #~ Left and Right cannot be the same set in a 1D domain
        #~ self._assert(LeftNeighborComponent == UnionFind.NOSET or RightNeighborComponent == UnionFind.NOSET or LeftNeighborComponent != RightNeighborComponent, "Left and Right cannot be the same set in a 1D domain.")
        NumNeighborComponents = len(NeighborComponents)
        
        if (NumNeighborComponents == 0):
            #~ Create a new component
            UF.MakeSet(idx)
        elif (NumNeighborComponents == 1):
            #~ Extend the one and only component in the neighborhood
            #~ Note that NeighborComponents[0] holds the root of a component, since we called Find() earlier to retrieve it
            UF.ExtendSetByID(NeighborComponents[0], idx)
        else:
            #~ Merge the two components on either side of the current point
            #~ The current point is a maximum. We look for the largest minimum on either side to pair with. That is the smallest hub.
            #~ We look for the lowest minimum first (the one that survives) to break the tie in case of equality: np.argmin returns the first occurence in this case.
            idxLowestNeighborComp = np.argmin(InputData[NeighborComponents])
            idxLowestMinimum = NeighborComponents[idxLowestNeighborComp]
            idxHighestMinimum = NeighborComponents[(idxLowestNeighborComp + 1) % 2]
            UF.ExtendSetByID(idxLowestMinimum, idx)
            UF.Union(idxHighestMinimum, idxLowestMinimum)
            
            #~ Record the two paired extrema: index of minimu, index of maximum, persistence value
            Persistence = InputData[idx] - InputData[idxHighestMinimum]
            ExtremaAndPersistence.append((idxHighestMinimum, Persistence))
            ExtremaAndPersistence.append((idx, Persistence))

    idxGlobalMinimum = UF.Find(0)
    ExtremaAndPersistence.append((idxGlobalMinimum, np.inf))
    #~ print("UF is left with %d sets." % UF.NumSets)
    #~ print("Global minimum at %d with value %g" % (idxGlobalMinimum, InputData[idxGlobalMinimum]))

    return ExtremaAndPersistence

