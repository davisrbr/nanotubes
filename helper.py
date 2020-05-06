from typing import NamedTuple, List, Tuple
from scipy.special import jv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from functools import reduce
from numpy import errstate,isneginf,array
from pathlib import Path
from typing import Dict, Callable, Tuple

# global a0 length
BASIS_A0 : int = 0.246 #nm

class chiralIndices(NamedTuple):
    n : int
    m : int

def chiralAngle(chiralIndices : NamedTuple) -> float:
    return np.arctan(np.sqrt(3)*chiralIndices.m /
                     (2*chiralIndices.n + chiralIndices.m))

def diameter(chiralIndices : NamedTuple) -> float:
    return BASIS_A0/np.pi * np.sqrt(chiralIndices.n**2
                                    + chiralIndices.m**2
                                    + chiralIndices.n*chiralIndices.m)

def spacingD1(angle : float, astar : float) -> float:
    '''spacing for l1 pattern from R=0'''
    return astar*np.cos(angle)

def spacingD2(angle : float, astar : float) -> float:
    '''spacing for l2 pattern from R=0'''
    return astar*np.cos((60*np.pi/180) - angle)

def spacingD3(angle : float, astar : float) -> float:
    '''spacing for l3 pattern from R=0'''
    return astar*np.cos((60*np.pi/180) + angle)

def spacingD4(angle : float, astar : float) -> float:
    '''spacing for l4 pattern from R=0'''
    return np.sqrt(3)*astar*np.cos((30*np.pi/180) - angle)

def l0_mesh(chiralIndices : NamedTuple, radius_spacing : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l0'''
    return np.abs(jv(0, radius_spacing))**2 

def l1_mesh(chiralIndices : NamedTuple, radius_spacing : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l1'''
    return np.abs(jv(chiralIndices.m, radius_spacing))**2 

def l2_mesh(chiralIndices : NamedTuple, radius_spacing : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l2'''
    return np.abs(jv(chiralIndices.n, radius_spacing))**2

def l3_mesh(chiralIndices : NamedTuple, radius_spacing : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l3'''
    return np.abs(jv(chiralIndices.n + chiralIndices.m, radius_spacing))**2 

def l4_mesh(chiralIndices : NamedTuple, radius_spacing : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l4'''
    return np.abs(jv(chiralIndices.n - chiralIndices.m, radius_spacing))**2 

@st.cache()
def fact_dict_loader() -> Dict[Tuple[int, int], int]:
    key_value = np.loadtxt("indices.csv", delimiter=",")
    fact_dict = { (int(n), int(m)) : int(v) for n, m, v in key_value}
    return fact_dict

@st.cache()
def diffract_plot(chiral_n : int, chiral_m : int, num_layer_lines : int, 
    scale : float, option : str, lines : str, factor : int) -> np.ndarray:

    # define indices from user input
    indices = chiralIndices(chiral_n  , chiral_m)

    # diameter of carbon nanotube
    d       = diameter(indices) 

    # chiral angle of carbon nanotube
    angle   = chiralAngle(indices) 

    diameter_mesh = np.linspace(-d, d, 1000) #nm
    radius_spacing = np.pi*diameter_mesh*scale
    diffraction_spacing = radius_spacing.copy()

    astar = BASIS_A0 #reciprocal_basis(indices) #BASIS_A0
    diffraction_distance = np.pi*d*scale/factor

    mesh_layers : Dict[int, Tuple[Callable, float]] = {
                                        0 : (l0_mesh, 0.0             ),
                                        1 : (l1_mesh, spacingD1(angle, astar)),
                                        2 : (l2_mesh, spacingD2(angle, astar)),
                                        3 : (l3_mesh, spacingD3(angle, astar)),
                                        4 : (l4_mesh, spacingD4(angle, astar)) }

    total_mesh = np.zeros((1000, 1000))

    #to include center layer line
    index_layers = lines == 'No'
    
    for i in range(index_layers, num_layer_lines+1):
        
        # Tuple[mesh_function, spacing in nm]
        layer_line_func, position = mesh_layers[i] 
            
        # assumed layer line spacing based on 600 grid spaced Y-axis
        pos_position_slice = int(np.floor(500*position/diffraction_distance+500))
        neg_position_slice = -int(np.floor(500*position/diffraction_distance-500))

        # if not, scale is too 'zoomed in' to appear on plot, do nothing to mesh for line
        if pos_position_slice+2 <=1000:
            # define layer n_th line
            layer_line = layer_line_func(indices, radius_spacing)

            #define slices to mesh
            diff_spacing_pos = slice(pos_position_slice-3, 
                                     pos_position_slice+3)        

            diff_spacing_neg = slice(neg_position_slice-3, 
                                  neg_position_slice+3)

            total_mesh[diff_spacing_pos, :] = total_mesh[diff_spacing_neg, :] = layer_line

    # if logarithmic
    if option == 'Contrast':
        with errstate(divide='ignore'):
            total_mesh = np.log10(total_mesh)
            total_mesh[isneginf(total_mesh)]=0.0

    return radius_spacing, diffraction_spacing, total_mesh 

@st.cache()
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()
