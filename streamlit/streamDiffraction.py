import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from helper import diffract_plot, chiralIndices, chiralAngle, \
        diameter, read_markdown_file, fact_dict_loader


unc_svg = open("North_Carolina_Tar_Heels_logo.svg").read()
PAGE_CONFIG = {"page_title": "Chiral Indices of CNTs",
               "page_icon": unc_svg,
               "layout": "centered"}  # compare w/ "wide"
st.beta_set_page_config(**PAGE_CONFIG)
st.set_option('deprecation.showPyplotGlobalUse', False)
# set page title
st.title('Electron diffraction of carbon nanotube given chiral indices')

# intro_markdown = read_markdown_file("info.md")
intro_markdown = '''
<details>
<summary>ℹ️ Info</summary>

This app displays the simulated electron diffraction pattern of carbon nanotubes as defined by [Qin 2006.](https://research.physics.unc.edu/lcqin/www1/papers/2007-Qin-PCCP.pdf)

See the sidebar to control the diffraction intensity (logarithmic vs linear) and the scaling of the plot (defaults to 2.46 nm).

To save an image, right click and save (on Desktop) or press and hold (on mobile).

💻 The code is available [here](https://github.com/davisrbr/CNT_general).

</details>
'''
st.markdown(intro_markdown, unsafe_allow_html=True)
st.markdown("---")

st.sidebar.markdown("## Plot Details")
st.sidebar.markdown("① ** Diffraction intensity **")
option = st.sidebar.selectbox(
        'Linear or contrast (logarithmic) diffraction intensity?',
        ('Linear', 'Contrast')
        )
st.sidebar.markdown("---")
st.sidebar.markdown("② ** Size scale of plot **")
scale = st.sidebar.slider(
        "Scale as fraction of 0.246 nm (smaller # is more 'zoomed' in)",
        0.1, 50.0, 10.0, 0.1
        )
st.sidebar.markdown("---")
st.sidebar.markdown("③ ** Include center layer line (l₀) **")
lines = st.sidebar.selectbox('Include center layer line', ('Yes', 'No'))


chiral_n = st.number_input("Chiral indice n", 0, 24, 20, 1)
chiral_m = st.number_input("Chiral indice m", 0, 24, 3, 1)
indices = chiralIndices(chiral_n, chiral_m)

with st.spinner(text='Plotting new state'):
    # get pre-calculated spacing factor, from eqn. (70) in Qin 2006.
    fact_dict = fact_dict_loader()

    if indices.m > indices.n:
        factor = fact_dict[(indices.n, indices.m)]
    else:
        factor = fact_dict[(indices.m, indices.n)]

    try:
        radius_spacing, diffraction_spacing, total_mesh = diffract_plot(
                indices.n, indices.m, 3, scale, option, lines, factor
                )
    except Exception as e:
        st.markdown(
                'Could not make diffraction plot for the chiral indices. '
                'Please try a different pair or try again.'
                f'{e}'
                )
        radius_spacing, diffraction_spacing = np.zeros(1000), np.zeros(1000)
        total_mesh = np.zeros((1000, 1000))
    plt.xticks([])
    plt.yticks([])
    plt.title(f'Chiral indices: [{indices.n},{indices.m}]      Diameter: {round(diameter(indices), 3)}   Helicity: {round(chiralAngle(indices)*180/np.pi, 3)} degrees')
    plt.pcolormesh(
            radius_spacing, diffraction_spacing, total_mesh, cmap='Blues'
            )
    plt.axis('equal')
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.tick_params(
            top='off', bottom='off', left='off',
            right='off', labelleft='off', labelbottom='on'
            )

    plt.show()
    st.pyplot()
