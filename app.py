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
    col1, col2 = st.columns(2)

    chosen_year = col1.slider("Choose a year", 2010, 2020, 2020)
    chosen_state = col2.selectbox("Choose state", list(energy_df["state"].unique()))

    map_plt, pie_plt = plot_map_pie(chosen_state, chosen_year)

    st.plotly_chart(map_plt, use_container_width=True)

    scttr_plt = plot_scatter(chosen_state)

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
