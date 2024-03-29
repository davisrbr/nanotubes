from typing import NamedTuple, Tuple, Dict, Callable
from scipy.special import jv
import numpy as np
import streamlit as st
from numpy import errstate, isneginf
from pathlib import Path


# global a0 length
BASIS_A0: int = 0.246  # nm


class chiralIndices(NamedTuple):
    n: int
    m: int


def chiralAngle(chiralIndices: NamedTuple) -> float:
    return np.arctan(np.sqrt(3)*chiralIndices.m /
                     (2*chiralIndices.n + chiralIndices.m))


def diameter(chiralIndices: NamedTuple) -> float:
    return BASIS_A0/np.pi * np.sqrt(chiralIndices.n**2
                                    + chiralIndices.m**2
                                    + chiralIndices.n*chiralIndices.m)


def spacingD1(angle: float, astar: float) -> float:
    '''spacing for l1 pattern from R=0'''
    return astar*np.cos(angle)


def spacingD2(angle: float, astar: float) -> float:
    '''spacing for l2 pattern from R=0'''
    return astar*np.cos((60*np.pi/180) - angle)


def spacingD3(angle: float, astar: float) -> float:
    '''spacing for l3 pattern from R=0'''
    return astar*np.cos((60*np.pi/180) + angle)


def spacingD4(angle: float, astar: float) -> float:
    '''spacing for l4 pattern from R=0'''
    return np.sqrt(3)*astar*np.cos((30*np.pi/180) - angle)


def l0_mesh(
        chiralIndices: NamedTuple, radius_spacing: np.ndarray
        ) -> np.ndarray:
    '''2D mesh of values for l0'''
    return np.abs(jv(0, radius_spacing))**2


def l1_mesh(
        chiralIndices: NamedTuple, radius_spacing: np.ndarray
        ) -> np.ndarray:
    '''2D mesh of values for l1'''
    return np.abs(jv(chiralIndices.m, radius_spacing))**2


def l2_mesh(
        chiralIndices: NamedTuple, radius_spacing: np.ndarray
        ) -> np.ndarray:
    '''2D mesh of values for l2'''
    return np.abs(jv(chiralIndices.n, radius_spacing))**2


def l3_mesh(
        chiralIndices: NamedTuple, radius_spacing: np.ndarray
        ) -> np.ndarray:
    '''2D mesh of values for l3'''
    return np.abs(jv(chiralIndices.n + chiralIndices.m, radius_spacing))**2


def l4_mesh(
        chiralIndices: NamedTuple, radius_spacing: np.ndarray
        ) -> np.ndarray:
    '''2D mesh of values for l4'''
    return np.abs(jv(chiralIndices.n - chiralIndices.m, radius_spacing))**2


@st.cache()
def fact_dict_loader() -> Dict[Tuple[int, int], int]:
    # key_value = np.loadtxt("indices.csv", delimiter=",")
    key_value = np.array([[  0.,   1.,  15.],
       [  1.,   1.,  15.],
       [  1.,   2.,  18.],
       [  1.,   3.,  24.],
       [  1.,   4.,  31.],
       [  1.,   5.,  37.],
       [  1.,   6.,  44.],
       [  1.,   7.,  51.],
       [  1.,   8.,  59.],
       [  1.,   9.,  68.],
       [  1.,  10.,  75.],
       [  1.,  11.,  79.],
       [  1.,  12.,  75.],
       [  1.,  13.,  82.],
       [  1.,  14.,  87.],
       [  1.,  15.,  90.],
       [  1.,  16.,  96.],
       [  1.,  17., 100.],
       [  1.,  18.,  96.],
       [  1.,  19., 100.],
       [  1.,  20., 103.],
       [  1.,  21., 108.],
       [  1.,  22., 114.],
       [  1.,  23., 121.],
       [  1.,  24., 121.],
       [  2.,   2.,  16.],
       [  2.,   3.,  21.],
       [  2.,   4.,  26.],
       [  2.,   5.,  30.],
       [  2.,   6.,  36.],
       [  2.,   7.,  42.],
       [  2.,   8.,  47.],
       [  2.,   9.,  52.],
       [  2.,  10.,  58.],
       [  2.,  11.,  63.],
       [  2.,  12.,  68.],
       [  2.,  13.,  71.],
       [  2.,  14.,  76.],
       [  2.,  15.,  81.],
       [  2.,  16.,  86.],
       [  2.,  17.,  93.],
       [  2.,  18.,  97.],
       [  2.,  19.,  99.],
       [  2.,  20., 103.],
       [  2.,  21., 108.],
       [  2.,  22., 114.],
       [  2.,  23., 122.],
       [  2.,  24., 121.],
       [  3.,   3.,  25.],
       [  3.,   4.,  30.],
       [  3.,   5.,  35.],
       [  3.,   6.,  40.],
       [  3.,   7.,  45.],
       [  3.,   8.,  50.],
       [  3.,   9.,  55.],
       [  3.,  10.,  60.],
       [  3.,  11.,  64.],
       [  3.,  12.,  71.],
       [  3.,  13.,  75.],
       [  3.,  14.,  80.],
       [  3.,  15.,  85.],
       [  3.,  16.,  90.],
       [  3.,  17.,  95.],
       [  3.,  18., 100.],
       [  3.,  19., 106.],
       [  3.,  20., 108.],
       [  3.,  21., 113.],
       [  3.,  22., 118.],
       [  3.,  23., 123.],
       [  3.,  24., 128.],
       [  4.,   4.,  34.],
       [  4.,   5.,  39.],
       [  4.,   6.,  44.],
       [  4.,   7.,  49.],
       [  4.,   8.,  54.],
       [  4.,   9.,  58.],
       [  4.,  10.,  61.],
       [  4.,  11.,  67.],
       [  4.,  12.,  71.],
       [  4.,  13.,  76.],
       [  4.,  14.,  81.],
       [  4.,  15.,  88.],
       [  4.,  16.,  94.],
       [  4.,  17.,  99.],
       [  4.,  18., 103.],
       [  4.,  19., 108.],
       [  4.,  20., 113.],
       [  4.,  21., 118.],
       [  4.,  22., 123.],
       [  4.,  23., 129.],
       [  4.,  24., 131.],
       [  5.,   5.,  43.],
       [  5.,   6.,  48.],
       [  5.,   7.,  52.],
       [  5.,   8.,  57.],
       [  5.,   9.,  63.],
       [  5.,  10.,  67.],
       [  5.,  11.,  70.],
       [  5.,  12.,  75.],
       [  5.,  13.,  80.],
       [  5.,  14.,  86.],
       [  5.,  15.,  91.],
       [  5.,  16.,  95.],
       [  5.,  17.,  99.],
       [  5.,  18., 104.],
       [  5.,  19., 109.],
       [  5.,  20., 115.],
       [  5.,  21., 120.],
       [  5.,  22., 125.],
       [  5.,  23., 130.],
       [  5.,  24., 134.],
       [  6.,   6.,  51.],
       [  6.,   7.,  56.],
       [  6.,   8.,  61.],
       [  6.,   9.,  66.],
       [  6.,  10.,  70.],
       [  6.,  11.,  76.],
       [  6.,  12.,  80.],
       [  6.,  13.,  85.],
       [  6.,  14.,  90.],
       [  6.,  15.,  95.],
       [  6.,  16., 101.],
       [  6.,  17., 106.],
       [  6.,  18., 111.],
       [  6.,  19., 115.],
       [  6.,  20., 120.],
       [  6.,  21., 125.],
       [  6.,  22., 130.],
       [  6.,  23., 136.],
       [  6.,  24., 140.],
       [  7.,   7.,  59.],
       [  7.,   8.,  64.],
       [  7.,   9.,  69.],
       [  7.,  10.,  74.],
       [  7.,  11.,  79.],
       [  7.,  12.,  84.],
       [  7.,  13.,  89.],
       [  7.,  14.,  93.],
       [  7.,  15.,  98.],
       [  7.,  16., 103.],
       [  7.,  17., 108.],
       [  7.,  18., 113.],
       [  7.,  19., 118.],
       [  7.,  20., 124.],
       [  7.,  21., 129.],
       [  7.,  22., 134.],
       [  7.,  23., 139.],
       [  7.,  24., 143.],
       [  8.,   8.,  68.],
       [  8.,   9.,  73.],
       [  8.,  10.,  78.],
       [  8.,  11.,  83.],
       [  8.,  12.,  88.],
       [  8.,  13.,  93.],
       [  8.,  14.,  98.],
       [  8.,  15., 103.],
       [  8.,  16., 107.],
       [  8.,  17., 112.],
       [  8.,  18., 117.],
       [  8.,  19., 122.],
       [  8.,  20., 128.],
       [  8.,  21., 131.],
       [  8.,  22., 135.],
       [  8.,  23., 139.],
       [  8.,  24., 141.],
       [  9.,   9.,  78.],
       [  9.,  10.,  83.],
       [  9.,  11.,  84.],
       [  9.,  12.,  90.],
       [  9.,  13.,  95.],
       [  9.,  14., 100.],
       [  9.,  15., 105.],
       [  9.,  16., 109.],
       [  9.,  17., 114.],
       [  9.,  18., 119.],
       [  9.,  19., 124.],
       [  9.,  20., 129.],
       [  9.,  21., 135.],
       [  9.,  22., 139.],
       [  9.,  23., 144.],
       [  9.,  24., 150.],
       [ 10.,  10.,  84.],
       [ 10.,  11.,  93.],
       [ 10.,  12.,  97.],
       [ 10.,  13., 101.],
       [ 10.,  14., 105.],
       [ 10.,  15., 110.],
       [ 10.,  16., 114.],
       [ 10.,  17., 118.],
       [ 10.,  18., 123.],
       [ 10.,  19., 127.],
       [ 10.,  20., 131.],
       [ 10.,  21., 135.],
       [ 10.,  22., 140.],
       [ 10.,  23., 145.],
       [ 10.,  24., 151.],
       [ 11.,  11.,  93.],
       [ 11.,  12.,  98.],
       [ 11.,  13., 102.],
       [ 11.,  14., 107.],
       [ 11.,  15., 112.],
       [ 11.,  16., 117.],
       [ 11.,  17., 122.],
       [ 11.,  18., 127.],
       [ 11.,  19., 132.],
       [ 11.,  20., 137.],
       [ 11.,  21., 141.],
       [ 11.,  22., 144.],
       [ 11.,  23., 148.],
       [ 11.,  24., 152.],
       [ 12.,  12., 103.],
       [ 12.,  13., 108.],
       [ 12.,  14., 112.],
       [ 12.,  15., 118.],
       [ 12.,  16., 123.],
       [ 12.,  17., 128.],
       [ 12.,  18., 131.],
       [ 12.,  19., 136.],
       [ 12.,  20., 140.],
       [ 12.,  21., 143.],
       [ 12.,  22., 148.],
       [ 12.,  23., 152.],
       [ 12.,  24., 158.],
       [ 13.,  13., 110.],
       [ 13.,  14., 115.],
       [ 13.,  15., 120.],
       [ 13.,  16., 124.],
       [ 13.,  17., 129.],
       [ 13.,  18., 134.],
       [ 13.,  19., 139.],
       [ 13.,  20., 144.],
       [ 13.,  21., 149.],
       [ 13.,  22., 153.],
       [ 13.,  23., 157.],
       [ 13.,  24., 161.],
       [ 14.,  14., 117.],
       [ 14.,  15., 122.],
       [ 14.,  16., 127.],
       [ 14.,  17., 132.],
       [ 14.,  18., 137.],
       [ 14.,  19., 142.],
       [ 14.,  20., 147.],
       [ 14.,  21., 152.],
       [ 14.,  22., 156.],
       [ 14.,  23., 161.],
       [ 14.,  24., 166.],
       [ 15.,  15., 127.],
       [ 15.,  16., 130.],
       [ 15.,  17., 134.],
       [ 15.,  18., 139.],
       [ 15.,  19., 144.],
       [ 15.,  20., 149.],
       [ 15.,  21., 154.],
       [ 15.,  22., 159.],
       [ 15.,  23., 164.],
       [ 15.,  24., 169.],
       [ 16.,  16., 134.],
       [ 16.,  17., 139.],
       [ 16.,  18., 144.],
       [ 16.,  19., 149.],
       [ 16.,  20., 154.],
       [ 16.,  21., 159.],
       [ 16.,  22., 164.],
       [ 16.,  23., 169.],
       [ 16.,  24., 174.],
       [ 17.,  17., 141.],
       [ 17.,  18., 144.],
       [ 17.,  19., 151.],
       [ 17.,  20., 156.],
       [ 17.,  21., 161.],
       [ 17.,  22., 166.],
       [ 17.,  23., 171.],
       [ 17.,  24., 176.],
       [ 18.,  18., 152.],
       [ 18.,  19., 157.],
       [ 18.,  20., 162.],
       [ 18.,  21., 166.],
       [ 18.,  22., 170.],
       [ 18.,  23., 175.],
       [ 18.,  24., 181.],
       [ 19.,  19., 162.],
       [ 19.,  20., 167.],
       [ 19.,  21., 172.],
       [ 19.,  22., 176.],
       [ 19.,  23., 181.],
       [ 19.,  24., 186.],
       [ 20.,  20., 168.],
       [ 20.,  21., 173.],
       [ 20.,  22., 178.],
       [ 20.,  23., 183.],
       [ 20.,  24., 188.],
       [ 21.,  21., 176.],
       [ 21.,  22., 181.],
       [ 21.,  23., 186.],
       [ 21.,  24., 191.],
       [ 22.,  22., 186.],
       [ 22.,  23., 191.],
       [ 22.,  24., 196.],
       [ 23.,  23., 196.],
       [ 23.,  24., 201.],
       [ 24.,  24., 206.],
       [  0.,   2.,  14.],
       [  0.,   3.,  19.],
       [  0.,   4.,  24.],
       [  0.,   5.,  30.],
       [  0.,   6.,  37.],
       [  0.,   7.,  43.],
       [  0.,   8.,  48.],
       [  0.,   9.,  55.],
       [  0.,  10.,  62.],
       [  0.,  11.,  69.],
       [  0.,  12.,  76.],
       [  0.,  13.,  86.],
       [  0.,  14.,  90.],
       [  0.,  15.,  93.],
       [  0.,  16., 100.],
       [  0.,  17., 108.],
       [  0.,  18., 115.],
       [  0.,  19., 122.],
       [  0.,  20., 129.],
       [  0.,  21., 137.],
       [  0.,  22., 144.],
       [  0.,  23., 152.],
       [  0.,  24., 160.],
       [  0.,  24., 160.]])

    fact_dict = {(int(n), int(m)): int(v) for n, m, v in key_value}
    return fact_dict


@st.cache()
def diffract_plot(
        chiral_n: int, chiral_m: int, num_layer_lines: int,
        scale: float, option: str, lines: str, factor: int
        ) -> np.ndarray:
    # define indices from user input
    indices = chiralIndices(chiral_n, chiral_m)
    # diameter of carbon nanotube
    d = diameter(indices)
    # chiral angle of carbon nanotube
    angle = chiralAngle(indices)

    diameter_mesh = np.linspace(-d, d, 1000)  # nm
    radius_spacing = np.pi*diameter_mesh*scale
    diffraction_spacing = radius_spacing.copy()

    astar = BASIS_A0  # BASIS_A0
    diffraction_distance = np.pi*d*scale/factor

    mesh_layers: Dict[int, Tuple[Callable, float]] = {
                                        0: (l0_mesh, 0.0),
                                        1: (l1_mesh, spacingD1(angle, astar)),
                                        2: (l2_mesh, spacingD2(angle, astar)),
                                        3: (l3_mesh, spacingD3(angle, astar)),
                                        4: (l4_mesh, spacingD4(angle, astar))}

    total_mesh = np.zeros((1000, 1000))
    max = 0.0
    for i in range(1, num_layer_lines+1):

        # Tuple[mesh_function, spacing in nm]
        layer_line_func, position = mesh_layers[i]

        # assumed layer line spacing based on 600 grid spaced Y-axis
        pos_position_slice = int(
                np.floor(500*position/diffraction_distance+500)
                )
        neg_position_slice = -int(
                np.floor(500*position/diffraction_distance-500)
                )

        # if not, scale is too 'zoomed in' to appear on plot, do nothing
        if pos_position_slice+2 <= 1000:
            # define layer n_th line
            layer_line = layer_line_func(indices, radius_spacing)
            test_max = np.max(layer_line)
            if test_max > max:
                max = test_max

            # define slices to mesh
            diff_spacing_pos = slice(pos_position_slice-3,
                                     pos_position_slice+3)
            diff_spacing_neg = slice(neg_position_slice-3,
                                     neg_position_slice+3)
            total_mesh[diff_spacing_pos, :] = layer_line
            total_mesh[diff_spacing_neg, :] = layer_line

    # include center lines
    if lines == 'Yes':
        layer_line_func, position = mesh_layers[0]

        # assumed layer line spacing based on 600 grid spaced Y-axis
        pos_position_slice = int(
                np.floor(500*position/diffraction_distance+500)
                )
        neg_position_slice = -int(
                np.floor(500*position/diffraction_distance-500)
                )

        # top hat function so intensity does not dominate
        prop_layer_line = layer_line_func(indices, radius_spacing)
        layer_line = np.piecewise(
                prop_layer_line,
                [prop_layer_line < max, prop_layer_line >= max],
                [lambda x: x, lambda x: max]
                )

        # define slices to mesh
        diff_spacing_pos = slice(pos_position_slice-3,
                                 pos_position_slice+3)
        diff_spacing_neg = slice(neg_position_slice-3,
                                 neg_position_slice+3)
        total_mesh[diff_spacing_pos, :] = layer_line
        total_mesh[diff_spacing_neg, :] = layer_line

    # if logarithmic
    if option == 'Contrast':
        with errstate(divide='ignore'):
            total_mesh = np.log10(total_mesh)
            total_mesh[isneginf(total_mesh)] = 0.0

    return radius_spacing, diffraction_spacing, total_mesh


@st.cache()
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()
