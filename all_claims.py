from initialize_date_and_crm import *
from detailed_claims import *

def fill_antecedents(current_crm, age_crm50, current_date_start, last_date_start):

    # Select CRM calculation method
    st.write("Méthode de saisie des sinistres survenus les 3 dernières années")
    calculation_method = st.radio(
        "Méthode de saisie des sinistres survenus les 3 dernières années",
        ["Détaillée", "Agrégée"],
        captions = [
            "Saisie des sinistres ligne à ligne",
            "Saisie directe du nombre de sinistres responsables"
            ],
        label_visibility='collapsed',
        horizontal=True
    )

    # Initialize date variables
    last_cutoff_start = (last_date_start-pd.DateOffset(months=2)).date()
    last_cutoff_end = (current_date_start-pd.DateOffset(months=2)-pd.DateOffset(days=1)).date()
    previous_cutoff_start = st.session_state.date_max-pd.DateOffset(years=3)
    previous_cutoff_end = (last_date_start-pd.DateOffset(months=2)-pd.DateOffset(days=1)).date()
    
    last_cutoff_start_str = convert_date_to_str(last_cutoff_start)
    last_cutoff_end_str = convert_date_to_str(last_cutoff_end)
    previous_cutoff_start_str = convert_date_to_str(previous_cutoff_start)
    previous_cutoff_end_str = convert_date_to_str(previous_cutoff_end)

    st.write(f'La période de référence pour le calcul du nouveau CRM correspond à la période du {last_cutoff_start_str} au {last_cutoff_end_str} (2 mois précédant le début du nouveau contrat).')

    if calculation_method == "Détaillée":
         df_claims = convert_to_date(fill_detailed_claims())
    else: df_claims = st.session_state.df_claims

    # Fully Responsible Claims
    fullyRespClaimCount_default = (
        (df_claims['claim_resp'] == 'Totale')*
        (df_claims['claim_date'] >= last_cutoff_start)*
        (df_claims['claim_date'] <= last_cutoff_end)
        ).sum()
    # Partially Responsible Claims
    partiallyRespClaimCount_default = (
        (df_claims['claim_resp'] == 'Partielle')*
        (df_claims['claim_date'] >= last_cutoff_start)*
        (df_claims['claim_date'] <= last_cutoff_end)
        ).sum()
    # Total Responsaible Claims
    totalRespClaimCount_default = fullyRespClaimCount_default+partiallyRespClaimCount_default
    # Ignored Responsible Claims
    ignoredRespClaimCount = 0
    
    # Is insured CRM 50 since at least 3Y
    B50_OlderThan3Y = (age_crm50 >= 3)

    if current_crm == 50 and B50_OlderThan3Y:

        if calculation_method == 'Détaillée':
            # Previous Responsible Claims
            previousRespClaimCount = (
                (df_claims['claim_resp'].isin(['Totale', 'Partielle']))*
                (df_claims['claim_date'] < previous_cutoff_end)
                ).sum()
            
            if previousRespClaimCount == 0:
                if totalRespClaimCount_default > 0:
                    st.write(f"Pas de sinistre responsable survenu du {previous_cutoff_start_str} au {previous_cutoff_end_str}.")
                    st.write(f"Le premier sinistre responsable survenu le {convert_date_to_str(df_claims.loc[df_claims['claim_date'].argmin(), 'claim_date'])} sur la période de référence est ignoré.")
                    df_claims = df_claims.drop(index=df_claims['claim_date'].argmin())
                    ignoredRespClaimCount += 1
                    totalRespClaimCount_default -= ignoredRespClaimCount
                    if totalRespClaimCount_default == 0:
                         st.write(f"Aucun autre sinistre responsable survenu du {last_cutoff_start_str} au {last_cutoff_end_str}. Pas de dégradation du CRM mais perte de l'ancienneté bonus 50.")
                    else:
                        if totalRespClaimCount_default == 1:
                            st.write(f"{totalRespClaimCount_default} autre sinistre responsable survenu du {last_cutoff_start_str} au {last_cutoff_end_str}. Dégradation du CRM.")
                        else: st.write(f"{totalRespClaimCount_default} autres sinistres responsables survenus du {last_cutoff_start_str} au {last_cutoff_end_str}. Dégradation du CRM.")
                    # Fully Responsible Claims
                    fullyRespClaimCount_default = (
                        (df_claims['claim_resp'] == 'Totale')*
                        (df_claims['claim_date'] >= last_cutoff_start)*
                        (df_claims['claim_date'] <= last_cutoff_end)
                        ).sum()
                    # Partially Responsible Claims
                    partiallyRespClaimCount_default = (
                        (df_claims['claim_resp'] == 'Partielle')*
                        (df_claims['claim_date'] >= last_cutoff_start)*
                        (df_claims['claim_date'] <= last_cutoff_end)
                        ).sum()
                else: st.write(f"Aucun sinistre responsable survenu depuis 3 ans. Pas d'impact sur l'ancienneté bonus 50.")
            else:
                if previousRespClaimCount == 1: st.write(f"1 sinistre responsable survenu du {previous_cutoff_start_str} au {previous_cutoff_end_str}.")
                else: st.write(f"{previousRespClaimCount} sinistres responsables survenus du {previous_cutoff_start_str} au {previous_cutoff_end_str}.")
                st.write("Tous les sinistres responsables survenus sur la période de référence sont pris en compte.")
        else: st.write("Les assurés ayant obtenu le bonus 50 depuis plus de 3 ans sont immunisés lors du premier sinistre responsable ou partiellement responsable survenu dans les 3 ans. Attention à ne pas le compter le cas échéant.")

    fullyRespClaim_col, partiallyRespClaim_col = st.columns(2)
    
    with fullyRespClaim_col:
        # Fully Responsible Claims
        st.write(f"Sinistres du {last_cutoff_start_str} au {last_cutoff_end_str} - Responsabilité totale")
        fullyRespClaimCount = st.number_input(
                    "Sinistres responsables",
                    min_value=0,
                    value=fullyRespClaimCount_default,
                    step=1,
                    disabled=(calculation_method == "Détaillée"),
                    label_visibility="collapsed"
                    )
    with partiallyRespClaim_col:
        # Partially Responsible Claims
        st.write(f"Sinistres du {last_cutoff_start_str} au {last_cutoff_end_str} - Responsabilité partielle")
        partiallyRespClaimCount = st.number_input(
                    "Sinistres partiellement responsables",
                    min_value=0,
                    value=partiallyRespClaimCount_default,
                    step=1,
                    disabled=(calculation_method == "Détaillée"),
                    label_visibility="collapsed"
                    )

    return fullyRespClaimCount, partiallyRespClaimCount, ignoredRespClaimCount