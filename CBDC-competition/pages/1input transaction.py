import streamlit as st
import pyodbc
import datetime
import pandas as pd

st.set_page_config(
    page_title="Input Transaction",
    page_icon="🍁",
)

# Input fields
sender = st.text_input("Sender Name:")
receiver_name = st.text_input("Receiver Name:")
senderId = st.number_input('SenderId', min_value=1, max_value=10,  step=1)
receiverId = st.number_input('ReceiverId', min_value=1, max_value=10,  step=1)
value = st.number_input('Value')

# File upload button
uploaded_file = st.file_uploader("Upload a CSV file")

insert_button = st.button("Insert Data")

# Connection string
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:cbdctest.database.windows.net,1433;Database=Transactions;Uid=CloudSA4ab3329e;Pwd=$sremmaH123456;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Insert data function
def insert_data(conn, cursor, senderId, receiverId, sender, receiver_name, value, timestamp):
    insert_query = 'INSERT INTO [Transactions].[Events] (SenderId, ReceiverId, SenderName, ReceiverName, Value, Timestamp) VALUES (?, ?, ?, ?, ?, ?)'
    cursor.execute(insert_query, senderId, receiverId, sender, receiver_name, value, timestamp)
    conn.commit()

# Streamlit app logic
if insert_button:
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        timestamp = datetime.datetime.utcnow()

        # Insert data using input fields
        insert_data(conn, cursor, senderId, receiverId, sender, receiver_name, value, timestamp)
        st.success('Data inserted successfully')

        cursor.close()
        conn.close()

    except Exception as e:
        st.error("Error inserting data:", e)

# Handle uploaded CSV file
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Display the uploaded data
        st.write("Uploaded Data:")
        st.write(df)

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        timestamp = datetime.datetime.utcnow()

        for index, row in df.iterrows():
            sender_name = row['SenderName']
            receiver_name = row['RecieverName']
            sender_id = row['SenderId']
            receiver_id = row['ReceiverId']
            value = row['Value']

            insert_data(conn, cursor, sender_id, receiver_id, sender_name, receiver_name, value, timestamp)

        cursor.close()
        conn.close()

        st.success('Uploaded data inserted successfully')

    except Exception as e:
        st.error("Error inserting uploaded data:", e)
