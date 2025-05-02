from initialize_globals import *


def initialize_date_and_crm_info():
    mode_col, period_start_col, last_period_start_col, current_crm_col = st.columns(4)

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

    with last_period_start_col:
        # Display last effective date
        match mode:
            case "Nouvelle souscription":
                st.write("Date d'édition du RI")
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
                st.write("CRM déclaré (%)")
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

    last_cutoff_start_str = convert_date_to_str(last_cutoff_start)
    last_cutoff_end_str = convert_date_to_str(last_cutoff_end)

    st.write(
        f"La période de référence pour le calcul du nouveau CRM correspond à la période du {last_cutoff_start_str} au {last_cutoff_end_str}."
    )
    if mode == "Nouvelle souscription" and last_period_months < 10:
        st.write(
            "Le CRM ne peut pas s'améliorer car elle s'étale sur moins de 10 mois."
        )
    if mode == "Police en portefeuille":
        st.write(
            "Les 2 derniers mois de la période en cours sont ignorés lors du renouvellement."
        )

    return (
        last_cutoff_start,
        last_cutoff_end,
        previous_cutoff_start,
        previous_cutoff_end,
        current_crm,
        age_crm50,
        last_period_months,
    )
