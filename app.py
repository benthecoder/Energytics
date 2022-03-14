import streamlit as st
from pages import *
from visualizations import *


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Energytics",
        page_icon="⚡",
        initial_sidebar_state="expanded",
        layout="wide",
    )

    pages = {
        "home": home_page,
        "prod": energy_prod,
        "cons": energy_cons,
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "home",
            }
        )

    local_css("style.css")

    with st.sidebar:
        st.caption("""Navigate the app 👇""")

        if st.button("🏠 Home"):
            st.session_state.page = "home"
        if st.button("🌊 🏭  Energy Production"):
            st.session_state.page = "prod"
        if st.button("🔌 🔋 Energy Consumption"):
            st.session_state.page = "cons"

    pages[st.session_state.page]()


if __name__ == "__main__":
    main()
