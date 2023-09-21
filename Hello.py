import streamlit as st
import snowflake.connector
import pandas as pd

# Snowflake credentials
snowflake_credentials = {
    'user': 'DEMOUSER',
    'password': 'Mattyice',
    'account': 'FV13022.east-us-2.azure',
    'warehouse': 'TRIAL_PRACTICE_WH',
    'database': 'HONEYCOMB',
    'schema': 'BIZDEV'
}

# Snowflake connection
conn = snowflake.connector.connect(**snowflake_credentials)
cursor = conn.cursor()

# Function to fetch data from Snowflake
def fetch_data():
    cursor.execute("SELECT * FROM SAMPLEDATA")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    return df

# Function to update data in Snowflake
def update_data(df):
    # Delete the existing data from the table
    cursor.execute("DELETE FROM SAMPLEDATA")
    
    # Insert the updated data
    for _, row in df.iterrows():
        cursor.execute(f"INSERT INTO SAMPLEDATA VALUES ({', '.join(['%s']*len(df.columns))})", tuple(row))

    conn.commit()

# Streamlit app
st.title("Moser BizDev Data Entry")

# Load data from Snowflake
data = fetch_data()


# Display the data in an editable DataFrame using st.data_editor
edited_data = st.data_editor(data, num_rows="dynamic")

# Update the data in Snowflake if any changes are made
if st.button("Save Changes"):
    update_data(edited_data)

# Close the Snowflake connection
cursor.close()
conn.close()
