from initialize_globals import *

# Main function to fill detailed claims
def fill_detailed_claims():

    # Retrieve the claims DataFrame
    st.session_state.df_claims = retrieve_df_claims()

    # Convert 'claim_date' column to datetime type
    st.session_state.df_claims = convert_to_date(st.session_state.df_claims)

    # Configure column settings for the data editor
    column_config = configure_column_config(st.session_state.date_min, 
                                            st.session_state.date_max, 
                                            ['Non responsable', 'Totale', 'Partielle'])

    # Display the data editor for claims input
    df_claims = display_data_editor(st.session_state.df_claims, column_config)

    return df_claims

# Function to retrieve the claims DataFrame
def retrieve_df_claims():
    return st.session_state.df_claims

# Function to convert 'claim_date' column to datetime type
def convert_to_date(df):
    if not df.empty:
        df['claim_date'] = pd.to_datetime(df['claim_date'], errors='coerce').dt.date
    return df

# Function to configure column settings for the data editor
def configure_column_config(date_min, date_max, resp_options):
    config = {
        'claim_date': st.column_config.DateColumn(
            'Date Sinistre', width='medium',
            format="DD/MM/YYYY", min_value=date_min, max_value=date_max,
            required=True, default=date_max
        ),
        'claim_resp': st.column_config.SelectboxColumn(
            'Responsabilité', width='medium',
            options=resp_options,
            required=True, default=resp_options[0]
        )
    }
    return config

# Function to display the data editor for claims input
def display_data_editor(df, column_config):
    st.write('Saisie des sinistres ligne à ligne')
    edited_df = st.data_editor(
        df.reset_index(drop=True),
        column_config=column_config,
        num_rows='dynamic',
        use_container_width=True
    )
    return edited_df