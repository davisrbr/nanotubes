import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from helper import diffract_plot, chiralIndices, chiralAngle, \
        diameter, read_markdown_file, fact_dict_loader


unc_svg = '''
<?xml version="1.0"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 170 134">\n<path d="m112.89 71.28-31.32-35.27c2.802-.213 5.639-.32 8.483-.32 8.867 0 17.68 1.061 25.663 3.083-1.918 9.139-2.892 18.621-2.892 28.228 0 1.427.023 2.857.065 4.285m-14.36 26.694c-2.813.214-5.648.323-8.482.323-8.868 0-17.682-1.061-25.665-3.082 1.922-9.136 2.894-18.62 2.894-28.228 0-1.428-.021-2.857-.065-4.285l31.318 35.272zm-60.69-15.9c-3.988-3.73-7.567-8.824-7.567-15.087 0-6.264 3.579-11.357 7.567-15.086.646 4.938.973 9.992.973 15.086s-.327 10.151-.973 15.087m113.56-6.15c-.538-.536-1.265-.833-2.014-.833-.108 0-.218.007-.328.019-.862.099-1.634.589-2.091 1.328-1.209 1.95-2.786 3.835-4.71 5.636-.645-4.936-.971-9.99-.971-15.083s.326-10.145.971-15.083c1.924 1.801 3.501 3.686 4.71 5.636.457.739 1.229 1.228 2.091 1.328.11.013.22.02.327.02.75 0 1.477-.299 2.015-.834l15.942-15.945c1.03-1.027 1.117-2.666.205-3.797-4.511-5.603-10.287-10.643-17.192-15.011 1.222-2.602 2.555-5.067 3.972-7.35.405-.651.529-1.438.345-2.183s-.661-1.383-1.321-1.77c-6.434-3.78-13.516-6.972-21.053-9.488-.295-.099-.601-.147-.901-.147-.989 0-1.934.517-2.455 1.406-1.529 2.608-2.975 5.356-4.318 8.192-10.943-3.152-22.56-4.748-34.575-4.748-10.585 0-20.918 1.247-30.744 3.713l-7.13-8.04c-.544-.619-1.324-.957-2.123-.957-.291 0-.585.044-.87.137-8.044 2.581-15.59 5.927-22.425 9.941-.734.432-1.237 1.17-1.37 2.012-.119.755.072 1.523.522 2.133 1.37 2.226 2.662 4.622 3.849 7.151-17.788 11.263-27.932 27.075-27.932 43.69 0 16.617 10.144 32.426 27.932 43.69-1.222 2.6-2.554 5.062-3.97 7.345-.404.653-.527 1.439-.344 2.184.184.743.66 1.383 1.322 1.772 6.431 3.777 13.515 6.97 21.049 9.486.298.1.603.146.901.146.989 0 1.935-.516 2.459-1.406 1.528-2.609 2.975-5.356 4.315-8.188 10.937 3.149 22.554 4.744 34.576 4.744 10.591 0 20.925-1.248 30.744-3.711l7.142 8.045c.55.619 1.328.956 2.128.956.29 0 .583-.043.872-.136 8.044-2.582 15.588-5.927 22.423-9.942.732-.432 1.234-1.168 1.37-2.008.118-.754-.071-1.523-.521-2.133-1.373-2.228-2.662-4.629-3.852-7.159 6.905-4.367 12.681-9.408 17.192-15.01.912-1.132.825-2.77-.205-3.797l-15.95-15.93z" fill="#13294B"/>\n<path fill="#7BAFD4" d="m140.2 87.45c-1.147-6.496-1.762-13.356-1.762-20.451 0-7.094.615-13.956 1.762-20.452 3.922 2.856 7.046 6.056 9.184 9.505l15.945-15.943c-4.783-5.939-11.104-11.239-18.603-15.68 1.547-3.565 3.28-6.903 5.182-9.967-6.225-3.657-13.111-6.77-20.512-9.242-1.89 3.225-3.634 6.631-5.22 10.189-10.973-3.421-23.214-5.339-36.128-5.339-11.208 0-21.91 1.443-31.714 4.059l-8.3-9.347c-7.884 2.538-15.224 5.808-21.824 9.686l.036.041c1.889 3.049 3.611 6.369 5.148 9.915-17.611 10.427-28.713 25.635-28.713 42.575 0 16.938 11.102 32.145 28.713 42.572-1.544 3.566-3.278 6.901-5.177 9.963 6.225 3.657 13.111 6.77 20.509 9.243 1.892-3.226 3.634-6.628 5.221-10.187 10.973 3.421 23.215 5.335 36.129 5.335 11.208 0 21.912-1.439 31.717-4.056l8.297 9.346c7.912-2.539 15.254-5.807 21.852-9.685l-.036-.041c-1.89-3.051-3.612-6.373-5.152-9.922 7.499-4.439 13.82-9.741 18.603-15.679l-15.94-15.954c-2.138 3.45-5.262 6.649-9.184 9.505m-100.3 0c-7.831-5.714-12.469-12.795-12.469-20.467 0-7.673 4.638-14.754 12.468-20.458 1.149 6.497 1.764 13.361 1.764 20.458s-.615 13.959-1.764 20.456m50.15 13.7c-10.479 0-20.352-1.406-29.031-3.888 2.212-9.522 3.412-19.697 3.412-30.268 0-4.175-.185-8.288-.548-12.324l40.467 45.58c-4.593.586-9.379.9-14.3.9m26.17-21.83-40.472-45.584c4.596-.585 9.383-.896 14.305-.896 10.479 0 20.352 1.406 29.031 3.887-2.211 9.524-3.412 19.698-3.412 30.27 0 4.174.186 8.287.548 12.323"/>\n</svg>
'''

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
