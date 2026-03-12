add_executable (MatplotlibVisualization MatplotlibVisualization.cpp)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/data.txt ${CMAKE_CURRENT_BINARY_DIR}/data.txt COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/visualize.py ${CMAKE_CURRENT_BINARY_DIR}/visualize.py COPYONLY)
