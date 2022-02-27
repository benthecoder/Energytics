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

    st.title("🌊 🏭 ⚡ Energytics  🔌 🔋")
    st.caption("Analytics and Insights for everything energy-related")

    st.subheader("Energy Production cost by State and Energy Source")

    st.caption(
        "We are using energy cost and production datasets in order to help energy companies decern what energy source would be most benficial for them to invest in."
    )

    chosen_year = st.slider("Choose a year", 2010, 2020, 2010)

    map_plt = plot_map(chosen_year)
    # source_plt = plot_src_map(chosen_year)

    st.plotly_chart(map_plt, use_container_width=True)

    st.markdown(
        """
    Form the plot, we can see that there are notably 3 main states in the US that are generating the most revenue year on year, with Texas ranking first, followed by California then Washington. 

    With Texas being the 2nd largest state in the US in terms of total land area,  the state is able to yield much crude oil and natural gas since the land is abundant of the fields.  The same reasoning resonates with California being the 2nd highest revenue generating state. 

    Looking closer to the map, we can also see that states in the middle of the US focuses more on generating revenue from wind energy.  This is evident because the annual average wind speed is highest and consistent at the middle of the US, reference [Annual average wind speed of the US at 80 m 5.  | Download Scientific Diagram](https://www.researchgate.net/figure/Annual-average-wind-speed-of-the-US-at-80-m-5_fig1_325422763)

    ---
    """
    )

    col1, col2 = st.columns(2)

    chosen_source = col1.selectbox(
        "Choose resource", list(energy_df["source"].unique())
    )

    chosen_year = col2.slider("Choose a year", 2010, 2020, 2010, key="map")

    st.plotly_chart(plot_src_map(chosen_year, chosen_source), use_container_width=True)

    st.markdown(
        """
        ---
        """
    )
    st.subheader("Getting a closer look at each state")

    col1, col2 = st.columns(2)

    chosen_state = col1.selectbox("Choose state", list(energy_df["state"].unique()))

    chosen_year = col2.slider("Choose a year", 2010, 2020, 2010, key="piechart")

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
