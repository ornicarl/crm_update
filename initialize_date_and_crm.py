from initialize_globals import *

def initialize_date_and_crm_info():

    current_date_start_col, last_date_start_col, current_crm_col = st.columns(3)

    with current_date_start_col:
        # Display target renewal date
        st.write("Début nouveau contrat")
        current_date_start = st.date_input(
            "Start date",
            min_value=st.session_state.date_today,
            format="DD/MM/YYYY",
            label_visibility="collapsed"
            )

    with last_date_start_col:
        # Display last effective date
        st.write("Début contrat actuel")
        last_date_start = st.date_input(
            "Last date",
            min_value=st.session_state.date_today-pd.DateOffset(years=1),
            value=current_date_start-pd.DateOffset(years=1),
            format="DD/MM/YYYY",
            label_visibility="collapsed"
            )

    with current_crm_col:
        # Fill current CRM
        st.write("CRM actuel (%)")
        current_crm = st.number_input(
            'CRM actuel', 
            min_value=50, 
            max_value=350,
            value=st.session_state.current_crm,
            step=5,
            label_visibility='collapsed'
            )
    
    if current_crm == 50:

        date_crm50_col, age_crm50_col = st.columns(2)

        with date_crm50_col:
        # Fill CRM 50% obtention date
            st.write("Date d'obtention du bonus 50")
            date_crm50 = st.date_input(
                "Date d'obtention du bonus 50",
                max_value=last_date_start,
                format="DD/MM/YYYY",
                label_visibility="collapsed"
                )
            
        with age_crm50_col:
            # Display age B50
            st.write("Ancienneté du bonus 50")
            age_crm50 = st.number_input(
                "Ancienneté du bonus 50",
                min_value=0,
                value=calculate_age(date_crm50, last_date_start),
                step=1,
                label_visibility="collapsed"
                )
    else: age_crm50 = 0
    
    return current_date_start, last_date_start, current_crm, age_crm50
