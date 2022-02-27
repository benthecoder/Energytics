import streamlit as st
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from visualizations import *
import datetime


def main():
    st.set_page_config(
        page_title="Energytics",
        page_icon="⚡",
        initial_sidebar_state="expanded",
        layout="wide",
    )

    st.title("🌊 🏭 ⚡ Energytics  🔌 🔋")
    st.caption("Analytics and Insights for everything energy-related")

    page = st.sidebar.radio(
        "Choose your page", ["Energy Production", "Energy Consumption"]
    )

    if page == "Energy Production":
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

        st.plotly_chart(
            plot_src_map(chosen_year, chosen_source), use_container_width=True
        )

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
    else:
        hist_plt = px.histogram(
            train,
            x="meter_reading",
            log_y=True,
            labels={
                "meter_reading": "Energy Consumption (kWh)",
                "count": "Count (log)",
            },
            title="Counts of Energy Consumption Readings",
        )

        hist_plt.update_layout(height=600, width=800)

        st.plotly_chart(hist_plt, use_container_width=True)

        plt.figure(figsize=(13, 6))
        sns.boxplot(data=train, x="primary_use", y="meter_reading")
        plt.xlabel("Building Usage")
        plt.ylabel("Energy Consumption (kWh)")
        plt.title("Energy Distribution based on Building Usage")
        plt.xticks(rotation=45)

        st.pyplot(plt)

        plt.figure(figsize=(13, 7))
        sns.set_theme()
        sns.boxplot(data=train, x="year_built", y="meter_reading")
        plt.xlabel("Year Building was Constructed")
        plt.ylabel("Energy Consumption (kWh)")
        plt.title("Energy Distribution based on Construction year")
        plt.xticks(rotation=45)

        st.pyplot(plt)

        plt.figure(figsize=(13, 7))
        sns.set_theme()
        sns.boxplot(data=train, x="cloud_coverage", y="meter_reading")
        plt.xlabel("Cloud Coverage")
        plt.ylabel("Energy Consumption (kWh)")
        plt.title("Energy consumption based on cloud coverage")
        st.pyplot(plt)

        fig = px.bar(
            train.groupby(["wind_speed", "wind_direction"]).mean().reset_index(),
            x="wind_speed",
            y="meter_reading",
            color="wind_speed",
            labels={
                "year_built": "Year building was constructed",
                "meter_reading": "Energy Consumption (kWh)",
            },
            title="Energy Consmption vs Wind Conditions",
            animation_frame="wind_direction",
            animation_group="wind_speed",
            range_y=[0, 450],
            range_x=[0, 20],
        )

        st.plotly_chart(fig, use_container_width=True)

        vars = st.selectbox("Choose variables to plot 👇", list(train.columns.values))
        st.pyplot(scatterplt(vars))

        st.markdown(
            """
        ---

        ## Predicting your Energy Consumption"""
        )

        loaded_model = joblib.load("model.sav")

        submit = False

        with st.form("company_info"):

            col1, col2 = st.columns(2)
            d = col1.date_input(
                "Choose a date where you want to predict energy for",
                datetime.date(2022, 2, 28),
            )
            hour = col2.number_input("Choose an hour too", min_value=0, max_value=23)

            week = d.isocalendar()[1]
            month = d.month
            day = d.day

            col1, col2 = st.columns(2)

            year = col1.number_input(
                "What year was the building built?",
                min_value=1968,
            )
            sq_feet = col2.number_input("Square feet", min_value=0)
            edu = st.checkbox(
                "Is your building used for education?", value=["yes", "no"]
            )

            user_input = [[sq_feet, week, year, edu, hour, month, day]]

            submitted = st.form_submit_button("Submit")

            if submitted:
                pred = loaded_model.predict(user_input)
                submit = True

        if submit is False:
            return

        st.subheader(
            f"The energy consumption of your building is {round(pred[0], 2)} kWh!"
        )


if __name__ == "__main__":
    main()
