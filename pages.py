import streamlit as st
import joblib
from visualizations import *
import datetime
from datetime import date
import holidays
from weather_api import get_weather_pred, weather_info
import numpy as np


def home_page():
    st.title("⚡ Energytics")

    st.subheader("Analytics and Insights for everything energy-related")

    st.image("media/energy.jpg", width=1000, use_column_width=True)

    st.markdown(
        """
        As it stands, fossil fuels are significantly cheaper at producing energy than renewable technologies. 
        
        However, this is not a sustainable solution, and we are still years away from reaching parity in efficiency between renewable sources and conventional fossil fuel sources.
        
         Moreover, businesses would not only profit from minimizing their energy consumption but also help them achieve lower CO2 emissions. 
         
         Our goal is to identify, through machine learning, which features contribute the most to energy consumption so that they can be tackled to minimize the energy consumption for businesses.
        """
    )


def energy_prod():
    st.subheader("Energy Production cost by State and Energy Source")

    st.caption(
        "We are using energy cost and production datasets in order to help energy companies discern what energy source would be most benficial for them to invest in."
    )

    chosen_year = st.slider("Choose a year", 2010, 2020, 2010)

    map_plt = plot_map(chosen_year)

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
        ### Data source  
        1. [U.S. Energy Information Administration](https://www.eia.gov/)
        1. [International Renewable Energy Agency (IRENA)](https://www.irena.org/)
        """
    )


def energy_cons():

    country_list = pd.read_pickle("data/country_list.pkl")
    prim_use = pd.read_pickle("data/primary_use.pkl")

    us_holidays = holidays.US()
    lgb1 = joblib.load("models/lgb1.pkl")
    lgb2 = joblib.load("models/lgb2.pkl")
    le = joblib.load("models/encoder.pkl")
    models = [lgb1, lgb2]

    meter_types = {"electricity": 0, "chilledwater": 1, "steam": 2, "hotwater": 3}

    st.markdown(
        """
        ## Predicting your Building's energy consumption

        We need some information from you to make an accurate prediction!

        First provide us a date you want to predict energy for, then provide us your location
        ---
        """
    )

    if "load_state" not in st.session_state:
        st.session_state.load_state = False

    with st.form("location"):

        col1, col2 = st.columns(2)

        d = col1.date_input(
            "Choose any date 30 days from today",
            date.today(),
            max_value=date.today() + datetime.timedelta(days=30),
        )

        hour = col2.number_input("Choose an hour too", min_value=0, max_value=23)

        col1, col2 = st.columns(2)
        zip_code = col1.text_input("Enter your ZIP Code")
        cnt_code = col2.selectbox("Enter your country", country_list)
        weather_input = {"zip_code": zip_code, "cnt_code": cnt_code}

        submitted = st.form_submit_button("Submit")

        if submitted or st.session_state.load_state is True:
            delta = d - date.today()
            day_from = delta.days  # get difference in days
            weather_pred = get_weather_pred(weather_input, local=True)
            st.session_state.load_state = True

    if st.session_state.load_state is False:
        return

    weather_dict = weather_info(weather_pred, day_from, hour)

    if weather_dict is None:
        return

    map = pd.DataFrame(
        [[weather_dict["lat"], weather_dict["lon"]]], columns=["lat", "lon"]
    )

    # plot map
    st.map(map)

    st.write(
        f"For the zip code {zip_code} in {cnt_code}, here's what we know about the weather on {d.strftime('%m/%d/%Y')} at hour {hour}"
    )

    st.markdown(
        f"""
        - It will be a day with {weather_dict['weather']['main']}, more specifically, {weather_dict['weather']['description']}
        - The low is {weather_dict['temp']['min'] } degrees and the high is {weather_dict['temp']['max']} degrees
        """
    )

    # save for model prediction
    wind_direction = weather_dict["wind_dir"]
    wind_speed = weather_dict["wind_speed"]
    air_temperature = weather_dict["air_temp"]

    st.subheader("This app isn't your weather channel, time to make predictions!")

    st.subheader("But first, some info about your building")

    submit = False

    with st.form("company_info"):

        col1, col2 = st.columns(2)
        primary_use = col1.selectbox("What is the use of the building?", prim_use)
        meter = col2.selectbox("What meter are you predicting for?", meter_types.keys())

        col1, col2 = st.columns(2)

        year_built = col1.number_input(
            "What year was the building built?",
            min_value=1968,
        )

        square_feet = col2.number_input("Square feet", min_value=0)

        floor_count = st.number_input("Floor count", min_value=0)

        is_holiday = 0
        if d in us_holidays:
            is_holiday = 1

        weekday = d.weekday()
        month = d.month
        day = d.day

        user_input = [
            [
                int(le.transform([primary_use])[0]),
                meter_types[meter],
                wind_direction,
                is_holiday,
                square_feet,
                year_built,
                air_temperature,
                floor_count,
                weekday,
                day,
                hour,
                month,
                wind_speed,
            ]
        ]

        submitted = st.form_submit_button("Submit")

        def get_energy_pred(features):
            res = np.expm1(sum(model.predict(features) for model in models) / 2)
            return round(res[0], 3)

        if submitted:
            # st.write(user_input)
            pred = get_energy_pred(user_input)
            st.success("Thanks for the information!")
            submit = True

    if submit is False:
        return

    st.subheader(f"The energy consumption of your building is {pred} kWh!")

    st.markdown(
        """
        ---
        ### Data Source 
        - [ASHRAE - Great Energy Predictor III](https://www.kaggle.com/c/ashrae-energy-prediction/data)
        ### Notebook for training the model
        - https://colab.research.google.com/drive/1b8RsxVAfBuSFnlijExt6Oef2ayF4hyFV?usp=sharing
    """
    )
