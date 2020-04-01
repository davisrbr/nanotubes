from typing import NamedTuple, List, Tuple
from scipy.special import jv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from functools import reduce
from numpy import errstate,isneginf,array
import pandas as pd
from pathlib import Path


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

def spacingD1(angle : float, scale : float) -> float:
    '''spacing for l1 pattern from R=0'''
    return BASIS_A0*scale*np.cos(angle)

def spacingD2(angle : float, scale : float) -> float:
    '''spacing for l2 pattern from R=0'''
    return BASIS_A0*scale*np.cos((60*np.pi/180) - angle)

def spacingD3(angle : float, scale : float) -> float:
    '''spacing for l3 pattern from R=0'''
    return BASIS_A0*scale*np.cos((60*np.pi/180) + angle)

def spacingD4(angle : float, scale : float) -> float:
    '''spacing for l4 pattern from R=0'''
    return np.sqrt(3)*BASIS_A0*scale*np.cos((30*np.pi/180) - angle)

def l0(chiralIndices : NamedTuple, X : np.ndarray,
      Y : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l0'''
    return np.abs(jv(0, X))**2 * Y

def l1(chiralIndices : NamedTuple, X : np.ndarray,
      Y : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l1'''
    return np.abs(jv(chiralIndices.m, X))**2 * Y

def l2(chiralIndices : NamedTuple, X : np.ndarray,
       Y : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l2'''
    return np.abs(jv(chiralIndices.n, X))**2 * Y

def l3(chiralIndices : NamedTuple, X : np.ndarray,
       Y : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l3'''
    return np.abs(jv(chiralIndices.n + chiralIndices.m, X))**2 * Y

def l4(chiralIndices : NamedTuple, X : np.ndarray, 
       Y : np.ndarray) -> np.ndarray:
    '''2D mesh of values for l4'''
    return np.abs(jv(chiralIndices.n - chiralIndices.m,X))**2 * Y

@st.cache()
def diffract_plot(chiral_n : int, chiral_m : int, 
    scale : float, option : str) -> np.ndarray:

    # define indices from user input
    indices = chiralIndices(chiral_n  , chiral_m)

    # diameter of carbon nanotube
    d       = diameter(indices) 

    # chiral angle of carbon nanotube
    angle   = chiralAngle(indices) 

    # D_i spacing of principal layer line i
    D3      = spacingD3(angle, scale)
    D2      = spacingD2(angle, scale)
    D1      = spacingD1(angle, scale)

    diffraction_distance = D1*600/500

    R = np.linspace(-d*4, d*4, 1000) #nm
    radius_spacing = 2*np.pi*R
    diffraction_spacing = np.linspace(-diffraction_distance, 
                                    diffraction_distance, 600)

    y_plot = np.full_like(diffraction_spacing, 0, dtype=np.double)

    #l0 centered
    D0spacing = slice(298, 302)
    y_plot[D0spacing] = 1
    (X,Y) = np.meshgrid(radius_spacing,y_plot)
    l0_mesh = l0(indices, X, Y)


    #l1 and D1
    D1spacing_pos = slice(int(300*D1/diffraction_distance+300)-2, 
                        int(300*D1/diffraction_distance+300)+2)
    y_plot[D1spacing_pos] = 1
    (X,Y) = np.meshgrid(radius_spacing,y_plot)
    l1_mesh_upper = l1(indices, X, Y)

    D1spacing_neg = slice(-int(300*D1/diffraction_distance-300)-2, 
                        -int(300*D1/diffraction_distance-300)+2)
    y_plot = np.full_like(diffraction_spacing, 0, dtype=np.double)
    y_plot[D1spacing_neg] = 1
    (X,Y) = np.meshgrid(radius_spacing,y_plot)
    l1_mesh_lower = l1(indices, X, Y)

    #l2 and D2
    D2spacing_pos = slice(int(300*D2/diffraction_distance+300)-2, 
                        int(300*D2/diffraction_distance+300)+2)
    y_plot = np.full_like(diffraction_spacing, 0, dtype=np.double)
    y_plot[D2spacing_pos] = 1
    (X,Y) = np.meshgrid(radius_spacing,y_plot)
    l2_mesh_upper = l2(indices, X, Y)

    D2spacing_neg = slice(-int(300*D2/diffraction_distance-300)-2, 
                        -int(300*D2/diffraction_distance-300)+2)
    y_plot = np.full_like(diffraction_spacing, 0, dtype=np.double)
    y_plot[D2spacing_neg] = 1
    (X,Y) = np.meshgrid(radius_spacing,y_plot)
    l2_mesh_lower = l2(indices, X, Y)

    #l3 and D3
    D3spacing_pos = slice(int(300*D3/diffraction_distance+300)-2, 
                        int(300*D3/diffraction_distance+300)+2)
    y_plot = np.full_like(diffraction_spacing, 0, dtype=np.double)
    y_plot[D3spacing_pos] = 1
    (X,Y) = np.meshgrid(radius_spacing,y_plot)
    l3_mesh_upper = l3(indices, X, Y)

    D3spacing_neg = slice(-int(300*D3/diffraction_distance-300)-2, 
                        -int(300*D3/diffraction_distance-300)+2)
    y_plot = np.full_like(diffraction_spacing, 0, dtype=np.double)
    y_plot[D3spacing_neg] = 1
    (X,Y) = np.meshgrid(radius_spacing,y_plot)
    l3_mesh_lower = l3(indices, X, Y)

    total_mesh = reduce(np.add, 
                        (l0_mesh+5,
                        l1_mesh_upper+5,l1_mesh_lower+5,
                        l2_mesh_upper+5,l2_mesh_lower+5,
                        l3_mesh_upper+5, l3_mesh_lower+5))

    # if logarithmic
    if option == 'Logarithmic':
        with errstate(divide='ignore'):
            total_mesh = np.log10(total_mesh)
            total_mesh[isneginf(total_mesh)]=0

    # plt.xticks([])
    # plt.yticks([])
    # plt.title(f'Chiral indices: [{indices.n},{indices.m}]      Diameter: {round(d, 3)}   Helicity: {round(angle*180/np.pi, 3)} degrees')
    # plt.pcolormesh(radius_spacing, diffraction_spacing, total_mesh,cmap='Blues')
    # plt.show()
    X,Y = np.meshgrid(radius_spacing, diffraction_spacing)
    return X, Y, total_mesh

@st.cache()
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()
