/*! \file MatplotlibVisualization.cpp
    Demonstrates how to run the C++ code and visualize the results using Matplotlib.
*/
/*! \example MatplotlibVisualization.cpp

    Demonstrates how to run the C++ code and visualize the results using Matplotlib.
        
    # Contents
    This example demonstrates how to:
    -# Read data from a file, 
    -# Use Persistence1D class to extract extrema
    -# Filter results according to persistence values.
    -# Visualize results using Matplotlib scripts.

    # Results Visualization
    -# Run visualize.py

    ## Matplotlib Plot of Results
    \image html MatplotlibVisRes.png "Matplotlib Plot of Results"
    \image latex MatplotlibVisRes.png "Matplotlib Plot of Results"

    # Code Documentation
*/

#include "persistence1d.hpp"
#include <fstream>

using namespace std;
using namespace p1d;

int main()
{
	//Input and class variables declaration
	Persistence1D p;
	vector<float> data;
	float currdata; 
	ifstream datafile;
	ofstream outfile;
	const char * filename = "data.txt";
	const char * outfilename = "res.txt";

	//Output variables declaration
	vector<int> min, max;			
	int globalMinIndex;
	
	//Open and read the data file
	datafile.open(filename);
	if (!datafile)
	{
		cout << "Cannot open data file for reading: " << filename << endl;
		return -1;
	}

	while(datafile >> currdata)
	{
		data.push_back(currdata);
	}
		
	datafile.close();
			
	//To start data processing, run persistence on data
	p.RunPersistence(data);

	//It is possible to verify the correctness of the results via sanity tests. 
	//Check the function documentation for further information.
	if (!p.VerifyResults()) 
	{
		cout << "ERROR" << endl;
	}
	
	//Now, set a threshold for features filtering
	float filterThreshold = 1.0;
	
	//Retrieve the filtered results from the class. 
	p.GetExtremaIndices(min, max, filterThreshold);
	globalMinIndex = p.GetGlobalMinimumIndex();
	
	//Print all found indices to a file
	outfile.open(outfilename);
	if (!outfile)
		return -2;
	
	for (unsigned int i = 0; i < min.size() && i < max.size(); i++)
	{
		outfile << min[i] << endl;
		outfile << max[i] << endl;
	}

	//Add the global minimum to the file as well:
	//The global minimum does is not returned via GetExtremaIndices, as it is not paired.
	outfile << globalMinIndex << endl;

	outfile.close();

	//To visualize the results:
	//Run visualize.py via Python, which can be found in the same folder as this file
	
	return 0;
}
