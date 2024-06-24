def calculate_crm(current_crm, fullyRespClaimCount, partiallyRespClaimCount, RespClaimSince3YCount, B50_OlderThan3Y):

    # parameters

    min_crm = 0.5
    max_crm = 3.5
    
    bonus = -0.05
    malus = 0.25
    
    # calculation

    adj_bonus = (1+bonus)**(fullyRespClaimCount+partiallyRespClaimCount==0)
    if B50_OlderThan3Y and RespClaimSince3YCount <= 1: adj_malus = 1
    else: adj_malus = (1+malus)**(fullyRespClaimCount) * (1+malus/2)**(partiallyRespClaimCount)

    adj_crm = adj_bonus * adj_malus
    new_crm = max(min(current_crm * adj_crm, max_crm), min_crm)

    return new_crm