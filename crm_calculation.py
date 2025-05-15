from datetime import UTC, datetime
from math import floor


def calculate_crm(
    current_crm, reference_period
):
    
    period_months = reference_period["period_months"]
    fullyRespClaimCount = reference_period["fullyRespClaimCount"]
    partiallyRespClaimCount = reference_period["partiallyRespClaimCount"]

    # parameters

    min_crm = 0.5
    max_crm = 3.5

    if period_months >= 10:
        bonus = -0.05
    else:
        bonus = 0
    malus = 0.25

    # calculation

    adj_bonus = (1 + bonus) ** (fullyRespClaimCount + partiallyRespClaimCount == 0)
    adj_malus = (1 + malus) ** (fullyRespClaimCount) * (1 + malus / 2) ** (
        partiallyRespClaimCount
    )

    adj_crm = adj_bonus * adj_malus
    new_crm = floor(100*max(min(current_crm * adj_crm, max_crm), min_crm))/100
    new_crm = max(min(int((current_crm * adj_crm) * 100 + 0.00001) / 100, max_crm), min_crm)

    return new_crm

CRM_MAX_PER_LICENCE_AGE_MAPPING = {
    0: 100,
    1: 95,
    2: 90,
    3: 85,
    4: 80,
    5: 76,
    6: 72,
    7: 68,
    8: 64,
    9: 60,
    10: 57,
    11: 54,
    12: 51,
}

def calculate_crm_max(driving_license_age: int):
    return CRM_MAX_PER_LICENCE_AGE_MAPPING.get(driving_license_age, 50)

