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
            current_crm,
            age_crm50,
            list_reference_periods,
            previous_cutoff_start,
            previous_cutoff_end,
        )
    )

    # Calculate and display new CRM
    new_crm = current_crm
    for reference_period, reference_period_idx in enumerate(list_reference_periods):
        
        st.write(
            f"Période de référence N°{reference_period_idx}."
        )
        
        new_crm = round(
            100
            * calculate_crm(
                new_crm / 100,
                reference_period
            ),
            0,
        )
        st.title(f"Nouveau CRM: {int(new_crm)}%")
        if new_crm == 50:
            if reference_period["ignoredRespClaimCount"] > 0 or new_crm > 50:
                new_age_crm50 = 0
            else:
                new_age_crm50 = age_crm50
    
    st.title(f"Ancienneté bonus 50: {new_age_crm50}")
