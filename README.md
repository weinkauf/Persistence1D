**Persistence1D** is a class for finding local extrema and their persistence 
in one-dimensional data. Local minima and local maxima are extracted, 
paired, and sorted according to their persistence.

The package supports C++, Python, and Matlab and comes with extensive documentation and examples.

Project homepage: http://www.csc.kth.se/~weinkauf/notes/persistence1d.html


**Reconstruct1D** is a tool for smoothing one-dimensional data based on topological constraints.
Consider some input data containing a number of local minima and maxima.
Given a selected subset of these minima/maxima, Reconstruct1D will produce a smoothed version of the input data with the following properties:

- the output data contains only the selected subset of minima/maxima,
- the output data is smooth in the sense of C1 or C2 continuity (user parameter),
- the output data is as close as desired to the original data (user parameter).

When working with noisy input data, the tool is best paired with Persistence1D, but it can just as well be used to create smooth one-dimensional data with topological constraints from scratch.

The package supports Python and Matlab.

Project homepage: http://www.csc.kth.se/~weinkauf/notes/reconstruct1d.html


The C++ and Matlab versions of Persistence1D/Reconstruct1D have been written by Yeara Kozlov and [Tino Weinkauf](http://www.csc.kth.se/~weinkauf/contact/), Max Planck Institute for Informatics, Saarbrücken, Germany. The Python version has been written by [Tino Weinkauf](http://www.csc.kth.se/~weinkauf/contact/), KTH Royal Institute of Technology, Stockholm, Sweden.

You may use it as you wish, it is in the public domain. If you find it useful, 
it would be nice to hear from you. Just drop us a line.
