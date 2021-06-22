# python_hackathon
Quantifying the interaction between blood vessels and neurons (Pablo Blinder's Lab)
using Napari visualization tool, to present the Dense Connectomic Reconstruction in Layer 4 of
the Somatosensory Cortex data (http://l4dense2019.brain.mpg.de/). 

The goal of this project is to calculate the minimal distance for each neuron node to the closest
blood vessel.

The data is composed of Dendrites and Axons, each with a list of nodes indicating their spatial position.

Analysis steps:
1. Loading the data for each neuron part (axon, dendrite).
2. Extracting the blood vessels coordinates.
2. Calculating the distance between each node to any blood vessel.
3. Saving the distance for the closest blood vessel of every node.

Running time issues:
Due to the huge amount of data and running time limitation,
we chose to calculate the distance for only 5 dendrites and 5 axons. 

In order to reduce the running time we decided to remove all internal points of a blood vessel,
with the understanding there is no need to calculate the distance to those points,
the shortest distance will surely be on the edges of the blood vessel.

Down sampling: 
All blood vessel points are located in a very dense way, so we decided to do a down sampling,
removing a point every 100 points.

Visualization:
 - how to use
 - what can we see

Requirements:
- napari
- os
- h5py
- numpy 
- matplotlib 
- scipy.ndimage 
- scipy.spatial 
- tqdm 

Optional packages for data download:
- directory_downloader 
- wget
- asyncio 

# Submitted by:
- Lior Sukman; 319124244; lior.sukman@gmail.com
- Adi Sarig; 204423875; adisarig105@gmail.com
- Inbal Zelig; 305063299; inbaladir@gmail.com
- Yossef Glantzspiegel; 207910928; yossef1@mail.tau.ac.il
- Mandy Rosemblaum; 305747230; mandyrosemblaum@gmail.com