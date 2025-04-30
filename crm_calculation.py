def calculate_crm(current_crm, fullyRespClaimCount, partiallyRespClaimCount, last_period_months):

    # parameters

    min_crm = 0.5
    max_crm = 3.5
    
    if last_period_months >= 10:
        bonus = -0.05
    else:
        bonus = 0
    malus = 0.25
    
    # calculation

    adj_bonus = (1+bonus)**(fullyRespClaimCount+partiallyRespClaimCount==0)
    adj_malus = (1+malus)**(fullyRespClaimCount) * (1+malus/2)**(partiallyRespClaimCount)

    adj_crm = adj_bonus * adj_malus
    new_crm = max(min(current_crm * adj_crm, max_crm), min_crm)

    return new_crm