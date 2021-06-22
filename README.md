# python_hackathon
Quantifying the interaction between blood vessels and neurons (Pablo Blinder's Lab)
using Napari visualization tool, to present the Dense Connectomic Reconstruction in Layer 4 of
the Somatosensory Cortex data (http://l4dense2019.brain.mpg.de/). 

## Submitted by:
- Lior Sukman; 319124244; lior.sukman@gmail.com
- Adi Sarig; 204423875; adisarig105@gmail.com
- Inbal Zelig; 305063299; inbaladir@gmail.com
- Yossef Glantzspiegel; 207910928; yossef1@mail.tau.ac.il
- Mandy Rosemblaum; 305747230; mandyrosemblaum@gmail.com

The goal of this project is to calculate the minimal distance for each node associated with a neuron to the closest
blood vessel.

The data is composed of dendrites and axons, each with a list of nodes indicating their spatial position, edges 
describing their structure and class describing their type (please refer to http://l4dense2019.brain.mpg.de/ to learn
about the possible classes).

Analysis steps:
1. Loading the data for the neuron part of choise (axon/ dendrite).
2. Extracting the blood vessels coordinates.
2. Calculating the distance between each node to any blood vessel.
3. Saving the distance to the closest blood vessel of every node.

Running time issues:
Due to the large amount of data and running time limitation,
we chose to calculate the distance for only 5 dendrites / 5 axons. 

In order to reduce the running time we decided to remove all internal points of a blood vessel, with the understanding
there is no need to calculate the distance to those points. This is True as the shortest distance will surely be on the
edges of the blood vessel.

Down sampling: 
All blood vessel points are located densely, so we decided to do a down sampling, removing a point every 100 points 
(i.e. leaving 1% of those points), this should have a neglectable effect on the results.

## Files And Modules:
* conf.py: This file contains various constant such as path to the data (make sure to update this according to the 
    setup on your machine), URLs for downloading the data, file names and more constants used, more description may
    be found inside.
* analysis/obj/node.py: Object describing nodes by x, y and z values. this also includes a field of distance that is
    later filled with the distance from the nearest blood vessel.
* analysis/obj/neuron_part.py: A file describing the basic data structure containing either the data for axons or 
    dendrites. It contains the fields: id (id of the axon / dendrite), class_type (class of the axon / dendrite),
    nodes ( a list of nodes as described in analysis/obj/node.py), edges (list of lists of size two of nodes
    rpresenting edges).
    * analysis/analyze.py: A file containing different calculations for the visualization. Please read ducomentation
        inside this file for further explanation.

Visualization:
This module consists of two important files:
    * visualization/vis_hdf.py: Visualize a blood vessel and its edges. This program opens a napari visualization window
        and is controlled by the following command line arguments:
        -file: str of the path to the hdf file wanted to be shown. Make sure that this is also the only file in 
        BLOOD_VESSEL_BOXES from conf (which holds the names of the blood-vessele hdf files to be read)
    * visualization/vis.py: This program opens a napari visualization window showing 5 dendrites / axons colored 
        accordind to their distance either from the origin or from the closest blood vessel. This is controlled by the
        following command line arguments:
        - is_axon: bool value with a default of True. When True axons are shown, otherwise dendrites are shown.
        - distance: bool value with a default of True. When True coloration is based on distance from neerest blood
            vessel, otherwise from the origin.
        When running the program, a naprai window will open, allowing filteration based on the class of the axons / 
        dendrites and based on nodes (points), or edges (vectors).
        Colors represent proximity to blood vessels and vary from green to purple.



## Requirements:
- napari
- os
- h5py
- numpy 
- matplotlib
- scipy
- tqdm 

### Optional packages for data download:
Note that the data in https://l4dense2019.rzg.mpg.de/webdav/ is assumed to be reachable, it is possible to download the
required files using fetch_data.py. To run it the following packages are required:
- directory_downloader 
- wget
- asyncio