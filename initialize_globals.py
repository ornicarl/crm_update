import streamlit as st
import pandas as pd
import datetime

# Function to initialize session state variables
def initialize_session_state():
    if 'init' not in st.session_state:
        # Initialize today date
        st.session_state.date_today = datetime.datetime.today()
        # Initialize CRM
        st.session_state.current_crm = 100
        # Flag to indicate initialization is complete
        st.session_state.init = True

def initialize_variables(date_start):
    # Initialize dates
    st.session_state.date_max = date_start-pd.DateOffset(days=1)
    st.session_state.date_min = st.session_state.date_max-pd.DateOffset(years=3)
    # Initialize the claims DataFrame
    st.session_state.df_claims = pd.DataFrame(columns=['claim_date', 'claim_resp'])

def calculate_age(date, date_today):
    age = date_today.year - date.year - ((date_today.month, date_today.day) < (date.month, date.day))
    return age