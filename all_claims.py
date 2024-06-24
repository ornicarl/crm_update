# Select CRM calculation method
from initialize_date_and_crm import *
from detailed_claims import *

def fill_antecedents(current_crm, date_last):
    st.write("Méthode de saisie des sinistres survenus les 3 dernières années")
    calculation_method = st.radio(
        "Méthode de saisie des sinistres survenus les 3 dernières années",
        ["Agrégée", "Détaillée"],
        captions = [
            "Saisie des sinistres ligne à ligne",
            "Saisie directe du nombre de sinistres"
            ],
        label_visibility='collapsed',
        horizontal=True
    )

    if calculation_method == "Détaillée":
        df_claims = fill_detailed_claims()
    else: df_claims = st.session_state.df_claims

    if current_crm == 50: fullyRespClaim_col, partiallyRespClaim_col, respClaimSince2Y_col = st.columns(3)
    else: fullyRespClaim_col, partiallyRespClaim_col = st.columns(2)

    with fullyRespClaim_col:
        # Fully Responsible Claims
        st.write("Sinistres période en cours - responsables")
        fullyRespClaimCount = st.number_input(
                    "Sinistres responsables",
                    min_value=0,
                    value=((df_claims['claim_resp'] == 'Totale')*
                           (convert_to_date(df_claims)['claim_date'] >= date_last)).sum(),
                    step=1,
                    label_visibility="collapsed"
                    )
    with partiallyRespClaim_col:
        # Partially Responsible Claims
        st.write("Sinistres période en cours - partiellement responsables")
        partiallyRespClaimCount = st.number_input(
                    "Sinistres partiellement responsables",
                    min_value=0,
                    value=((df_claims['claim_resp'] == 'Partielle')*
                           (convert_to_date(df_claims)['claim_date'] >= date_last)).sum(),
                    step=1,
                    label_visibility="collapsed"
                    )
    if current_crm == 50:
        with respClaimSince2Y_col:
            # Partially Responsible Claims
            st.write("Sinistres périodes antérieures - responsables")
            respClaimSince2YCount = st.number_input(
                        "Sinistres périodes antérieures - responsables",
                        min_value=0,
                        value=((df_claims['claim_resp'] == 'Totale')*
                               (convert_to_date(df_claims)['claim_date'] < date_last)).sum(),
                        step=1,
                        label_visibility="collapsed"
                        )
    else: respClaimSince2YCount = 0

    return fullyRespClaimCount, partiallyRespClaimCount, respClaimSince2YCount