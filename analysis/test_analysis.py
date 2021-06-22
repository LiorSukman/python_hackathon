from analysis.obj.node import Node
from analysis.obj.axon import Axon
from analysis.obj.dendrite import Dendrite
from analysis import analyze as az
import numpy as np
import h5py
from random import random
import pytest

DATA_BASE_PATH = r'C:\research papers\hackathon_project'
AXONS_FILE_PATH = f'{DATA_BASE_PATH}/axons.hdf5'
DENDRITES_FILE_PATH = f'{DATA_BASE_PATH}/dendrites.hdf5
BLOOD_VESSEL_BOXES_BASE_PATH = f'{DATA_BASE_PATH}/blood-vessel-segmentation'

# test Node
Node1 = Node((1,2,3), 12345678)
Node2 = Node((random(), random(), random()), 234456789)
def test_Node1():
    assert (type(Node1.x) == int and type(Node1.y == int) and type(Node1.z) == int)
    assert (type(Node2.x) == int and type(Node2.y == int) and type(Node2.z) == int)
    assert Node1.node_id != Node2.node_id
    assert ((Node1.distance < 0) and (Node2.distance < 0))

def test_Node2():
    Node1.update_distance_from_blood_vessel(100)
    Node2.update_distance_from_blood_vessles(100)
    assert(Node1.distance == Node2.distance)
    Node2.update_distance_from_blood_vessles(2)
    assert(Node1.distance != Node2.distance)

def test_Node3():
    s1 = "(1,2,3)"
    assert Node1.__str__() == s1

#test axon loading
def test_load_axons():
    axons_data = h5py.File(AXONS_FILE_PATH)
    all_axons = axons_data['axons']['skeleton']
    classes = axons_data['axons']['class']
    assert all_axons != classes
#test axon
loaded_axons = az.load_axons()
axon1 = loaded_axons['1']
axon2 = loaded_axons['10']
def test_Axon():
    assert axon1.id != axon2.id
    assert axon1.axon_type == axon2.axon_type
    assert axon1.nodes != axon2.nodes
    assert axon1.edges != axon2.edges

#test dendrite
def test_Dendrite():
    pass

