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

    # Fill antecedents
    list_reference_periods = (
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
    next_age_crm50 = age_crm50
    for reference_period_idx, reference_period in enumerate(list_reference_periods, 1):
        
        next_crm = round(
            100
            * calculate_crm(
                next_crm / 100,
                reference_period
            ),
            0,
        )
        st.title(f"Nouveau CRM période N°{reference_period_idx}: {int(next_crm)}%")
    
        if next_crm == 50:
            if reference_period["ignoredRespClaimCount"] > 0 or next_crm > 50:
                next_age_crm50 = 0
            else:
                next_age_crm50 += 1
            st.title(f"Ancienneté bonus 50 période N°{reference_period_idx}: {next_age_crm50}")
