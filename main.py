from initialize_date_and_crm import *
from all_claims import *
from crm_calculation import *


def main():
    
    # Initialize session state variables
    initialize_session_state()

    # Display and store target Start Date current CRM infos
    current_date_start, last_date_start, current_crm, age_crm50 = initialize_date_and_crm_info()

    # Initialize session state variables
    initialize_periods(current_date_start, age_crm50)

    # Fill antecedents
    fullyRespClaimCount, partiallyRespClaimCount, ignoredRespClaimCount = fill_antecedents(current_crm, age_crm50, current_date_start, last_date_start)

    # Calculate and display new CRM
    new_crm = round(100*calculate_crm(current_crm/100, fullyRespClaimCount, partiallyRespClaimCount), 0)
    st.title(f'Nouveau CRM: {int(new_crm)}%')
    if new_crm == 50:
        if ignoredRespClaimCount > 0 or current_crm > 50:
            new_age_crm50 = 0
        else: new_age_crm50 = age_crm50
        st.title(f'Ancienneté bonus 50: {new_age_crm50}')