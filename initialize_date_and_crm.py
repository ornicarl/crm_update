from datetime import timedelta
from math import ceil
from crm_calculation import calculate_crm_max
from initialize_globals import *


def initialize_date_and_crm_info():

    mode_col, period_start_col = st.columns(2)

    with mode_col:
        mode = st.radio(
            "Transaction", ["Nouvelle souscription", "Police en portefeuille"]
        )

    with period_start_col:
        # Display policy period start
        match mode:
            case "Nouvelle souscription":
                st.write("Effet nouveau contrat")
            case "Police en portefeuille":
                st.write("Effet nouvelle période")
        period_start_date = st.date_input(
            "Start date", format="DD/MM/YYYY", label_visibility="collapsed"
        )


    driving_license_col, last_period_start_col, current_crm_col = st.columns(3)

    with driving_license_col:
        # Display policy period start
        st.write("Permis obtenu le")
        driving_license_date = st.date_input(
            "Driving license date",
            format="DD/MM/YYYY",
            min_value=period_start_date - pd.DateOffset(years=70),
            value=period_start_date - pd.DateOffset(years=1),
            label_visibility="collapsed"
        )

    with last_period_start_col:
        # Display last effective date
        match mode:
            case "Nouvelle souscription":
                st.write("Date du CRM")
                last_period_start_date = st.date_input(
                    "Last date",
                    min_value=period_start_date - pd.DateOffset(years=10),
                    value=period_start_date - pd.DateOffset(years=1),
                    format="DD/MM/YYYY",
                    label_visibility="collapsed",
                )
            case "Police en portefeuille":
                st.write("Effet période précédente")
                last_period_start_date = st.date_input(
                    "Last date",
                    min_value=period_start_date - pd.DateOffset(years=1),
                    value=period_start_date - pd.DateOffset(years=1),
                    format="DD/MM/YYYY",
                    label_visibility="collapsed",
                )

    with current_crm_col:
        # Fill CRM
        match mode:
            case "Nouvelle souscription":
                st.write("CRM indiqué sur le RI (%)")
            case "Police en portefeuille":
                st.write("CRM actuel (%)")
        current_crm = st.number_input(
            "CRM actuel",
            min_value=50,
            max_value=350,
            value=st.session_state.current_crm,
            step=5,
            label_visibility="collapsed",
        )

    if current_crm == 50:
        date_crm50_col, age_crm50_col = st.columns(2)

        with date_crm50_col:
            # Fill CRM 50% obtention date
            st.write("Date d'obtention du bonus 50")
            date_crm50 = st.date_input(
                "Date d'obtention du bonus 50",
                max_value=last_period_start_date,
                format="DD/MM/YYYY",
                label_visibility="collapsed",
            )

        with age_crm50_col:
            # Display age B50
            st.write("Ancienneté du bonus 50")
            age_crm50 = st.number_input(
                "Ancienneté du bonus 50",
                min_value=0,
                value=calculate_age(date_crm50, last_period_start_date),
                step=1,
                label_visibility="collapsed",
            )
    else:
        age_crm50 = 0

    # Initialize session state variables
    match mode:
        case "Nouvelle souscription":
            reference_period_ignored_months = 0
        case "Police en portefeuille":
            reference_period_ignored_months = 2

    initialize_periods(period_start_date, age_crm50, reference_period_ignored_months)

    # Initialize CRM reference period
    last_cutoff_start = (
        last_period_start_date - pd.DateOffset(months=reference_period_ignored_months)
    ).date()
    last_cutoff_end = (
        period_start_date
        - pd.DateOffset(months=reference_period_ignored_months)
        - pd.DateOffset(days=1)
    ).date()
    previous_cutoff_start = st.session_state.date_max - pd.DateOffset(years=3)
    previous_cutoff_end = (
        last_period_start_date
        - pd.DateOffset(months=reference_period_ignored_months)
        - pd.DateOffset(days=1)
    ).date()
    last_period_months = (last_cutoff_end.year - last_cutoff_start.year) * 12 + (
        last_cutoff_end.month - last_cutoff_start.month
    )

    current_driving_license_age = max(calculate_age(driving_license_date, previous_cutoff_end), 0)
    current_crm_max = calculate_crm_max(current_driving_license_age)
    last_period_start_date_str = convert_date_to_str(last_period_start_date)

    if driving_license_date > last_period_start_date:
        st.write(
            f":red[L'obtention du permis ne peut pas être antérieure au dernier contrat d'assurance.]",
        )
    if current_crm < current_crm_max:
        st.write(
            f":red[Le CRM actuel optimal compte tenu de l'ancienneté du permis au {last_period_start_date_str} ({current_driving_license_age} ans) est {current_crm_max}.]",
        )
    
    list_reference_periods = []
    match mode:
        
        case "Nouvelle souscription":
            count_reference_periods = ceil(last_period_months/12)
            next_cutoff_start = last_cutoff_start
            for reference_period_idx in range(count_reference_periods):
                next_cutoff_end = min(
                    (next_cutoff_start.replace(year=next_cutoff_start.year + 1) - timedelta(days=1)),
                    last_cutoff_end
                )
                next_period_months = (next_cutoff_end.year - next_cutoff_start.year) * 12 + (
                    next_cutoff_end.month - next_cutoff_start.month
                )
                reference_period = {
                    "cutoff_start": next_cutoff_start,
                    "cutoff_end": next_cutoff_end,
                    "period_months": next_period_months
                }
                list_reference_periods.append(reference_period)
                next_cutoff_start = next_cutoff_start.replace(year=next_cutoff_start.year + 1)

        case "Police en portefeuille":
            reference_period = {
                "cutoff_start": last_cutoff_start,
                "cutoff_end": last_cutoff_end,
                "period_months": last_period_months
            }
            list_reference_periods.append(reference_period)

    for reference_period_idx, reference_period in enumerate(list_reference_periods, 1):

        cutoff_start_str = convert_date_to_str(reference_period["cutoff_start"])
        cutoff_end_str = convert_date_to_str(reference_period["cutoff_end"])

        st.write(
            f"La période de référence N°{reference_period_idx} pour le calcul du nouveau CRM correspond à la période du {cutoff_start_str} au {cutoff_end_str}."
        )
        if mode == "Nouvelle souscription" and reference_period["period_months"] < 9:
            st.write(
                f"Le CRM ne peut pas s'améliorer sur la période de référence N°{reference_period_idx} car elle s'étale sur moins de 9 mois."
            )
        if mode == "Police en portefeuille":
            st.write(
                "Les 2 derniers mois de la période en cours sont ignorés lors de la mise à jour du CRM lors du renouvellement."
            )

    return (
        list_reference_periods,
        previous_cutoff_start,
        previous_cutoff_end,
        current_crm,
        age_crm50,
    )
