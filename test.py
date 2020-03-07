from time import time

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def mpl_scatter(dataset, x, y):
    fig, ax = plt.subplots()
    dataset.plot.scatter(x=x, y=y, alpha=0.8, ax=ax)
    return fig


def altair_scatter(dataset, x, y):
    plot = (
        alt.Chart(dataset, height=400, width=400)
        .mark_point(filled=True, opacity=0.8)
        .encode(x=x, y=y)
    )
    return plot


size = st.slider("Size", min_value=1000, max_value=100_000, step=10_000)
dataset = pd.DataFrame(
    {"x": np.random.normal(size=size), "y": np.random.normal(size=size)}
)

mpl_start = time()
mpl_plot = mpl_scatter(dataset, "x", "y")
mpl_finish = time()

st.pyplot(mpl_plot)
mpl_render = time()
st.subheader("Matplotlib")
st.write(f"Create: {mpl_finish - mpl_start:.3f}s")
st.write(f"Render: {mpl_render - mpl_finish:.3f}s")
st.write(f"Total: {mpl_render - mpl_start:.3f}s")

alt_start = time()
alt_plot = altair_scatter(dataset, "x", "y")
alt_finish = time()

st.altair_chart(alt_plot)
alt_render = time()
st.subheader("Altair")
st.write(f"Create: {alt_finish - alt_start:.3f}s")
st.write(f"Render: {alt_render - alt_finish:.3f}s")
st.write(f"Total: {alt_render - alt_start:.3f}s")

speedup = (mpl_render - mpl_start) / (alt_render - alt_start)
st.write(f"MPL / Altair Ratio: {speedup:.1f}x")
