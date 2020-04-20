import matplotlib.pyplot as plt

def GetMinimaMaximaIndices(ExtremaAndPersistence):
    MinimaIdx = [t[0] for t in ExtremaAndPersistence[::2]]
    MaximaIdx = [t[0] for t in ExtremaAndPersistence[1::2]]
    return (MinimaIdx, MaximaIdx)

def Visualize(Data, ExtremaAndPersistence, FigAx = None, Style = 'data extrema', DataLabel = None, bShow = False, SaveFilename = None):
    
    SizeFactor = 1.5 if ('fat' in Style) else 0.5 if ('thin' in Style) else 1.0
    DashedDotted = 'dashed' if ('dashed' in Style) else 'dotted' if ('dotted' in Style) else 'solid'
    
    
    #~ Define colors and other style choices
    LineStyle = dict(color=(0.0, 0., 0.), linewidth=1*SizeFactor, linestyle=DashedDotted)
    MarkerStyleMinima = dict(linestyle='', markersize=8*SizeFactor, color=(0.3, 0.3, 1.0))
    MarkerStyleMaxima = dict(linestyle='', markersize=8*SizeFactor, color=(1.0, 0.2, 0.2))

    #~ Create Plot
    if FigAx == None:
        fig, ax = plt.subplots()
        fig.set_size_inches(19.20/2, 10.80/2, forward=True)
        fig.set_dpi(200)
        fig.set_tight_layout(True)
        #~ ax.grid()
    else:
        fig, ax = FigAx

    #~ Plot the data as a line plot
    if ('data' in Style):
        ax.plot(range(0, len(Data)), Data, **LineStyle, label=DataLabel)

    #~ Plot the MinimaIdx and MaximaIdx
    if ('extrema' in Style):
        #~ Get the indices of the minima and maxima as well as the global minimum
        (MinimaIdx, MaximaIdx) = GetMinimaMaximaIndices(ExtremaAndPersistence)
        #~ Actually plot them
        ax.plot(MinimaIdx, Data[MinimaIdx], marker='.', **MarkerStyleMinima)
        ax.plot(MaximaIdx, Data[MaximaIdx], marker='.', **MarkerStyleMaxima)

    #~ Set some labels and grid
    ax.set(xlabel='data index', ylabel='data value')
    ax.set_aspect(1.0/ax.get_data_ratio()*0.2)    
    
    # Place a legend above this subplot, expanding itself to fully use the given bounding box.
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)    

    #~ Save picture as PNG and show the interactive window
    if SaveFilename != None:
        fig.savefig(SaveFilename)
        print("Saved visualization as %s" % SaveFilename)
    if (bShow):
        plt.show()
        
    return (fig, ax)
