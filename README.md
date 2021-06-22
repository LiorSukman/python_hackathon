# python_hackathon
Quantifying the interaction between blood vessels and neurons (Pablo Blinder's Lab)
using Napari visualization tool, to present the Dense Connectomic Reconstruction in Layer 4 of
the Somatosensory Cortex data (http://l4dense2019.brain.mpg.de/). 

The goal of this project is to calculate the minimal distance for each neuron node to the closest
blood vessel.

Analysis steps:
1. Loading the data for each neuron part (axon, dendrite) and making a list of the nodes it's composed of
2. Extracting the blood vessels coordinates
2. Calculating the distance between each node and blood vessel
3. Saving the minimum distance for each node

Running time issues:
Due to running time limitation, we chose to show the heatmap distance matrix for
only 5 dendrites and 5 axons. 

Due to long running time we decided to remove all inside indices of a blood vessel,
with the understanding there is no need to calculate the distance to those indices,
the shortest distance will surely be on the edges of the blood vessel.

Down sampling: 
All blood vessel indices are located in a very dense way, so we decided to do a down sampling,
removing an index every 100 indices.

Visualization:
 - how to use
 - what can we see

Requirements:
- asyncio
- directory_downloader 
- wget
- os
- h5py
- numpy 
- matplotlib 
- scipy.ndimage 
- scipy.spatial 
- tqdm 

# Submitted by:
- Lior Sukman; 319124244; lior.sukman@gmail.com
- Adi Sarig; 204423875; adisarig105@gmail.com
- Inbal Zelig; 305063299; inbaladir@gmail.com
- Yossef Glantzspiegel; 207910928; yossef1@mail.tau.ac.il
- Mandy Rosemblaum; 305747230; mandyrosemblaum@gmail.com