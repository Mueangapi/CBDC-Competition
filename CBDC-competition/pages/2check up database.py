import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(
    page_title="query from database",
    page_icon="🍁",
)

connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:cbdctest.database.windows.net,1433;Database=Transactions;Uid=CloudSA4ab3329e;Pwd=$sremmaH123456;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Fetch data from the table
cursor.execute('SELECT * FROM Transactions.Events')
data = cursor.fetchall()

# Get column names from the cursor description


# Create a DataFrame from the data
df = pd.DataFrame(data)


# Display the data in the Streamlit app
st.write("Events:")
st.dataframe(df)

# Close the connection
cursor.close()
conn.close()
