# Outil de recalcul du CRM (Bonus-Malus) pour l’assurance auto

Cet outil interactif (Streamlit) permet aux gestionnaires d’assurance de recalculer le CRM lors de la validation d’un contrat auto, pour une nouvelle souscription ou un renouvellement.

## Fonctionnalités

- Prise en compte du type de contrat (nouvelle souscription/renouvellement)
- Saisie des dates clés (RI, dates d’effet)
- Calcul intelligent de la période de référence
- Blocage automatique du bonus si la période < 9 mois pour les nouvelles souscriptions
- Saisie détaillée ou agrégée des sinistres
- Calcul conforme aux règles légales du CRM

## Installation

```bash
git clone <url-du-repo>
cd <nom-du-repo>
pip install -r requirements.txt
```

## Utilisation

```
streamlit run streamlit_app.py
```

Suivez les instructions à l’écran pour saisir les informations et obtenir le nouveau CRM.

## Structure du code

- main.py : point d’entrée principal, logique de flux.
- initialize_date_and_crm.py : gestion de la saisie des dates et des périodes.
- all_claims.py / detailed_claims.py : saisie des sinistres et agrégation.
- crm_calculation.py : calcul du CRM selon les règles métier.
- initialize_globals.py : gestion de l’état de session et fonctions utilitaires.

## Contribution

Les PR sont les bienvenues. Merci de documenter toute règle métier spécifique dans le code et dans ce README.

## Licence
MIT