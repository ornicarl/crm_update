from initialize_date_and_crm import *
from all_claims import *
from crm_calculation import *


def main():
    
    # Initialize session state variables
    initialize_session_state()

    # Display and store target Start Date current CRM infos
    date_start, date_last, current_crm, age_crm50 = initialize_date_and_crm_info()

    # Initialize session state variables
    initialize_variables(date_start)

    # Fill antecedents
    fullyRespClaimCount, partiallyRespClaimCount, respClaimSince2YCount = fill_antecedents(current_crm, date_last)

    # Calculate and display new CRM
    new_crm = int(100*calculate_crm(
        current_crm/100,
        fullyRespClaimCount, 
        partiallyRespClaimCount,
        respClaimSince2YCount,
        age_crm50 >= 3
        ))
    st.title(f'New CRM: {new_crm}%')