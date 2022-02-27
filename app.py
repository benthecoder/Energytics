import streamlit as st
import streamlit.components.v1 as components

from visualizations import *


def main():
    st.set_page_config(
        page_title="Energytics",
        page_icon="⚡",
        initial_sidebar_state="expanded",
        layout="wide",
    )

    st.title("Energytics")
    st.caption("Analytics and Insights for everything energy-related")

    st.subheader("Energy Production cost by State and Energy Source")

    st.caption(
        "We are using energy cost and production datasets in order to help energy companies decern what energy source would be most benficial for them to invest in."
    )

    chosen_year = st.slider("Choose a year", 2010, 2020, 2020)

    map_plt = plot_map(chosen_year)
    # source_plt = plot_src_map(chosen_year)

    st.plotly_chart(map_plt, use_container_width=True)

    col1, col2 = st.columns(2)

    chosen_source = col1.selectbox(
        "Choose resource", list(energy_df["source"].unique())
    )

    chosen_year = col2.slider("Choose a year", 2010, 2020, 2020, key="map")

    st.plotly_chart(plot_src_map(chosen_year, chosen_source), use_container_width=True)

    st.subheader("Getting a closer look at each state")

    col1, col2 = st.columns(2)

    chosen_state = col1.selectbox("Choose state", list(energy_df["state"].unique()))

    chosen_year = col2.slider("Choose a year", 2010, 2020, 2020, key="piechart")

    scttr_plt, pie_plt = plot_scatter_pie(chosen_state, chosen_year)

    st.plotly_chart(pie_plt, use_container_width=True)
    st.plotly_chart(scttr_plt, use_container_width=True)

    st.markdown(
        """
    ---
    ### Datasets we used to build this 
    1. [U.S. Energy Information Administration](https://www.eia.gov/)
    1. [International Renewable Energy Agency (IRENA)](https://www.irena.org/)
    """
    )


if __name__ == "__main__":
    main()
