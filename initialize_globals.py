import streamlit as st
import pandas as pd
import datetime


# Function to initialize session state variables
def initialize_session_state():
    if "init" not in st.session_state:
        # Initialize today date
        st.session_state.date_today = datetime.datetime.today()
        # Initialize CRM
        st.session_state.current_crm = 100
        # Initialize the claims DataFrame
        st.session_state.df_claims = pd.DataFrame(columns=["claim_date", "claim_resp"])
        # Flag to indicate initialization is complete
        st.session_state.init = True


def initialize_periods(date_start, last_date_start, age_crm50, reference_period_ignored_months):
    # Initialize dates
    st.session_state.date_max = date_start
    if age_crm50 == 0:
        st.session_state.date_min = min(
            (st.session_state.date_max - pd.DateOffset(years=3)).date(),
            last_date_start
        )
    else:
        st.session_state.date_min = min(
            (st.session_state.date_max
            - pd.DateOffset(years=1)
            - pd.DateOffset(months=reference_period_ignored_months)).date(),
            last_date_start
        )


def calculate_age(date, date_today):
    age = (
        date_today.year
        - date.year
        - ((date_today.month, date_today.day) < (date.month, date.day))
    )
    return age


def convert_date_to_str(date):
    date_str = f"{str(date)[8:10]}/{str(date)[5:7]}/{str(date)[:4]}"
    return date_str
