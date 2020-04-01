from typing import NamedTuple, List, Tuple
from scipy.special import jv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from functools import reduce
from numpy import errstate,isneginf,array
from helper import diffract_plot, chiralIndices, chiralAngle, diameter, read_markdown_file
import altair as alt
import pandas as pd

# set page title
st.title('Electron diffraction of carbon nanotube given chiral indices')

intro_markdown = read_markdown_file("info.md")
st.markdown(intro_markdown, unsafe_allow_html=True)
st.markdown("---")
# st.subheader('From Qin, L.-C., 2006, Rep. Prog. Phys. 69, 2761')


st.sidebar.markdown("## Plot Details")
st.sidebar.markdown("① ** Diffraction intensity **")
option = st.sidebar.selectbox('Logarithmic or linear diffraction intensity?', ('Logarithmic', 'Linear'))
st.sidebar.markdown("---")
st.sidebar.markdown("② ** Size scale of plot **")
scale = st.sidebar.slider("Scale as fraction of 0.246 nm", 0.1, 10.0, 1.0, 0.1)


chiral_n = st.number_input("Chiral indice n", 0, 35, 17, 1)
chiral_m = st.number_input("Chiral indice m", 0, 35, 2, 1)
indices  = chiralIndices(chiral_n, chiral_m)


radius_spacing, diffraction_spacing, total_mesh = diffract_plot(indices.n, indices.m, scale, option)
# source = pd.DataFrame({'x': x.ravel(),
#                      'y': y.ravel(),
#                      'z': z.ravel()})

# alt.data_transformers.disable_max_rows()
# c = alt.Chart(source).mark_rect().encode(
#     x=alt.X('x:O', axis=alt.Axis(labels=False)),
#     y=alt.Y('y:O',axis=alt.Axis(labels=False)), 
#     color=alt.Color('z:Q',legend=None)
# )

# st.altair_chart(c)
plt.xticks([])
plt.yticks([])
plt.title(f'Chiral indices: [{indices.n},{indices.m}]      Diameter: {round(diameter(indices), 3)}   Helicity: {round(chiralAngle(indices)*180/np.pi, 3)} degrees')
plt.pcolormesh(radius_spacing, diffraction_spacing, total_mesh,cmap='Blues')
plt.show()
st.pyplot()

# scale = st.slider("Scale as fraction of 0.246 nm", 0.1, 10.0, 1.0, 0.1)
# st.slider(l"Scale", min_value=None, max_value=None, value=None, step=None, format=None, key=None)

# st.write(D1/diffraction_distance, D2/diffraction_distance,D3/diffraction_distance)
# st.write(D1, D2, D3)