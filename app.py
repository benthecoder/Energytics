import streamlit as st

from visualizations import *


def main():
    st.set_page_config(
        page_title="Energytics",
        page_icon="⚡",
        initial_sidebar_state="expanded",
    )

    st.title("App title")
    st.caption("Words about the app")


if __name__ == "__main__":
    main()
