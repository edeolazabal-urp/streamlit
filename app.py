import calendar  # Import the calendar module

import altair as alt
import pandas as pd
from vega_datasets import data

import streamlit as st

st.set_page_config(layout="wide")

unemployment_df = data.unemployment_across_industries()

industries = sorted(unemployment_df["series"].unique())
years = sorted(unemployment_df["year"].unique())

columns = st.columns([2, 2], gap="large")
sidebar = st.sidebar


with sidebar:
    industry = st.selectbox("Industria", industries)
    year_selected = st.multiselect("Año", years, default=years)
    m_start, m_end = st.select_slider(
        "Meses",
        options=[i for i in range(1, 13)],
        value=(1, 12),
        format_func=lambda x: calendar.month_abbr[x],
    )

with columns[0]:
    filter_df = unemployment_df.loc[
        (unemployment_df["series"] == industry)
        & (unemployment_df["year"].isin(year_selected))
        & (unemployment_df["month"].between(m_start, m_end))
    ]
    st.dataframe(
        filter_df[["month", "year", "count", "rate"]],
        use_container_width=True,
        hide_index=True,
    )

with columns[1]:
    chart = (
        alt.Chart(filter_df)
        .mark_line()
        .encode(
            x=alt.X("month", title="Mes", type="nominal"),
            y=alt.Y("rate", title="Tasa de desempleo", type="quantitative"),
            color=alt.Color("year", title="Año", type="nominal"),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    tabs = st.tabs(industries)
    for idx, i in enumerate(industries):
        with tabs[idx]:
            st.subheader(i)
            chart = (
                alt.Chart(unemployment_df.loc[(unemployment_df["series"] == i)])
                .mark_line().encode(x=alt.X("month", title="Mes", type="nominal"),y=alt.Y("rate", title="Tasa de desempleo", type="quantitative"),               color=alt.Color("year", title="Año", type="nominal"),
                )
            )
            st.altair_chart(chart, use_container_width=True)
