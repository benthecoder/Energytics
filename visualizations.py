import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import datetime
import random
import os
import seaborn as sns
import matplotlib.pyplot as plt


energy_df = pd.read_csv("data/energy_cost.csv")
train = pd.read_csv("data/Ashrae/buildings_train.csv")

# get total revenue by year and state
sum_rev = energy_df.groupby(["year", "state", "code"]).sum().reset_index()
sum_rev.rename({"revenue": "sum_revenue"}, axis=1, inplace=True)

source_names = [
    "Coal",
    "Geothermal",
    "Hydroelectric Conventional",
    "Natural Gas",
    "Other Biomass",
    "Petroleum",
    "Solar Thermal and Photovoltaic",
    "Wind",
]

# merge it with original dataframe
df_sum = pd.merge(
    energy_df,
    sum_rev,
    how="left",
    on=["year", "state", "code"],
    suffixes=("", "_drop"),
)
# drop duplicate columns
df_sum.drop([col for col in df_sum.columns if "drop" in col], axis=1, inplace=True)

# calculate percentages
df_sum["source_perc"] = round((df_sum["revenue"] / df_sum["sum_revenue"]) * 100, 3)

# get percenrtage of revenue by source
state_perc = df_sum.pivot(
    index=["year", "state", "code"], columns="source", values="source_perc"
).reset_index()

# turn percentage of each source into a list
state_perc_dict = state_perc.T.to_dict()
state_perc_dict = {k: list(v.values()) for k, v in state_perc_dict.items()}
source_perc_list = list(state_perc_dict.values())
perc_vals = [src[3:] for src in source_perc_list]

sum_rev["source_perc"] = perc_vals


def hover_label(row):
    state = f"<b>{row['state']}</b><br><br>"

    sources = row["source_perc"]

    Coal = f"Coal: {0 if np.isnan(sources[0]) else sources[0]}% <br>"
    Geothermal = f"Geothermal: {0 if np.isnan(sources[1]) else sources[1]}% <br>"
    Hydroelectric = (
        f"Hydroelectric Conventional: {0 if np.isnan(sources[2]) else sources[2]}% <br>"
    )
    Natural = f"Natural Gas: {0 if np.isnan(sources[3]) else sources[3]}% <br>"
    Other = f"Other Biomass: {0 if np.isnan(sources[4]) else sources[4]}% <br>"
    Petroleum = f"Petroleum: {0 if np.isnan(sources[5]) else sources[5]}% <br>"
    Solar = f"Solar Thermal and Photovoltaic:  {0 if np.isnan(sources[6]) else sources[6]}% <br>"
    Wind = f"Wind: {0 if np.isnan(sources[7]) else sources[7]}% <br>"

    return (
        state
        + Coal
        + Geothermal
        + Hydroelectric
        + Natural
        + Other
        + Petroleum
        + Solar
        + Wind
    )


def plot_map(year: int):

    map_df = sum_rev.groupby(["year"]).filter(lambda x: (x["year"] == year).any())

    map_fig = go.Figure(
        data=go.Choropleth(
            locations=map_df["code"],
            z=map_df["sum_revenue"] * 1e6,
            text=map_df.apply(lambda row: hover_label(row), axis=1),
            hoverinfo="text",
            locationmode="USA-states",
            colorscale="Greens",
            autocolorscale=False,
            marker_line_color="darkgray",
            marker_line_width=0.5,
            colorbar_tickprefix="$",
            colorbar_title="Revenue<br>billions US$",
        )
    )

    map_fig.update_layout(
        title_text=f"Energy Production Revenue by State for {year}",
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(type="albers usa"),
            showcoastlines=False,
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
        ),
        annotations=[
            dict(
                x=0,
                y=-0.05,
                xref="paper",
                yref="paper",
                text="Source: U.S. Energy Information Administration & International Renewable Energy Agency (IRENA)",
                showarrow=False,
            )
        ],
        width=1700,
        height=800,
    )

    return map_fig


def plot_src_map(year: int, source: str):

    df_filter_year = energy_df.groupby(["year"]).filter(
        lambda x: (x["year"] == year).any()
    )

    df_filter_source = df_filter_year.groupby(["source"]).filter(
        lambda x: (x["source"] == source).any()
    )

    fig = go.Figure(
        data=go.Choropleth(
            locations=df_filter_source["code"],
            z=df_filter_source["generation"],
            text=df_filter_source.apply(
                lambda row: f"{row['state']}<br></br>{row['generation']} Megawatthours",
                axis=1,
            ),
            hoverinfo="text",
            locationmode="USA-states",
            colorscale="Reds",
            autocolorscale=False,
            marker_line_color="darkgray",
            marker_line_width=0.5,
            colorbar_title="Generation<br>Kilowatthours",
        )
    )

    fig.update_layout(
        title_text=f"Energy Generation for {source} in {year}",
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(type="albers usa"),
            showcoastlines=False,
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
        ),
        width=1700,
        height=800,
    )

    return fig


def plot_scatter_pie(state: str, year: str):

    df_state = energy_df.groupby(["state"]).filter(
        lambda x: (x["state"] == state).any()
    )
    df_total_rev = df_state.groupby(["year"]).sum().reset_index()
    df_total_rev.rename(
        {"year": "Years", "revenue": "Total Revenue ($1 million)"}, axis=1, inplace=True
    )

    map_df = sum_rev.groupby(["year"]).filter(lambda x: (x["year"] == year).any())
    pie_df = map_df.groupby(["state"]).filter(lambda x: (x["state"] == state).any())

    sctr_fig = px.line(
        df_total_rev,
        x="Years",
        y="Total Revenue ($1 million)",
        title=f"Total Revenue Over the Years for {state}",
    )

    pie_fig = px.pie(
        pie_df,
        values=pie_df["source_perc"].tolist()[0],
        names=source_names,
        title=f"Percentage of Revenue from Resource for {state} in {year}",
    )

    pie_fig.update_layout(
        width=1000,
        height=500,
    )

    return sctr_fig, pie_fig


def scatterplt(var):
    plt.figure(figsize=(13, 7))
    sns.set_theme()
    sns.scatterplot(data=train, x=var, y="meter_reading", alpha=0.1)
    x_label = var
    plt.xlabel(x_label)
    plt.ylabel("Energy Consumption (kWh)")
    plt.title("Energy consumption based on" + str(x_label))
    return plt
