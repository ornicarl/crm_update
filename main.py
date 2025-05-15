from initialize_date_and_crm import *
from all_claims import *
from crm_calculation import *


def main():
    # Initialize session state variables
    initialize_session_state()

    # Display and store target Start Date current CRM infos
    (
        list_reference_periods,
        previous_cutoff_start,
        previous_cutoff_end,
        current_crm,
        age_crm50,
    ) = initialize_date_and_crm_info()

    st.write(list_reference_periods)

    # Fill antecedents
    list_reference_periods_with_claims = (
        fill_antecedents(
            list_reference_periods,
            previous_cutoff_start,
            previous_cutoff_end,
            current_crm,
            age_crm50,
        )
    )

    # Calculate and display new CRM
    next_crm = current_crm
    for reference_period_idx, reference_period in enumerate(list_reference_periods_with_claims):
        
        st.write(
            f"Période de référence N°{reference_period_idx}."
        )
        
        next_crm = round(
            100
            * calculate_crm(
                next_crm / 100,
                reference_period
            ),
            0,
        )
        st.title(f"Nouveau CRM: {int(next_crm)}%")
        if next_crm == 50:
            if reference_period["ignoredRespClaimCount"] > 0 or next_crm > 50:
                next_age_crm50 = 0
            else:
                next_age_crm50 = age_crm50
    
    st.title(f"Ancienneté bonus 50: {next_age_crm50}")
