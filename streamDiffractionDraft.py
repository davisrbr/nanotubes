from typing import NamedTuple, List, Tuple
from scipy.special import jv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from functools import reduce
from numpy import errstate,isneginf,array
from helper import diffract_plot, chiralIndices, chiralAngle, diameter, read_markdown_file

# set page title
st.title('Electron diffraction of carbon nanotube given chiral indices')

intro_markdown = read_markdown_file("info.md")
st.markdown(intro_markdown, unsafe_allow_html=True)
st.markdown("---")
# st.subheader('From Qin, L.-C., 2006, Rep. Prog. Phys. 69, 2761')


st.sidebar.markdown("## Plot Details")
st.sidebar.markdown("① ** Diffraction intensity **")
option = st.sidebar.selectbox('Logarithmic or linear diffraction intensity?', ('Linear', 'Logarithmic'))
st.sidebar.markdown("---")
st.sidebar.markdown("② ** Size scale of plot **")
scale = st.sidebar.slider("Scale as fraction of 0.246 nm", 0.1, 50.0, 10.0, 0.1)


chiral_n = st.number_input("Chiral indice n", 0, 35, 17, 1)
chiral_m = st.number_input("Chiral indice m", 0, 35, 2, 1)
indices  = chiralIndices(chiral_n, chiral_m)


with st.spinner(text='Plotting new chiral indices'):
                                                                                        #num_layer_lines here
    radius_spacing, diffraction_spacing, total_mesh = diffract_plot(indices.n, indices.m, 3, scale, option)
    plt.xticks([])
    plt.yticks([])
    plt.title(f'Chiral indices: [{indices.n},{indices.m}]      Diameter: {round(diameter(indices), 3)}   Helicity: {round(chiralAngle(indices)*180/np.pi, 3)} degrees')
    plt.pcolormesh(radius_spacing, diffraction_spacing, total_mesh,cmap='Blues')
    plt.show()
    st.pyplot()

# scale = st.slider("Scale as fraction of 0.246 nm", 0.1, 10.0, 1.0, 0.1)
# st.slider(l"Scale", min_value=None, max_value=None, value=None, step=None, format=None, key=None)