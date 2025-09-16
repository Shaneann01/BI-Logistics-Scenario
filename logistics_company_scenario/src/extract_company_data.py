import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

# Load environment variables
load_dotenv()
HOSTNAME = os.getenv("HOSTNAME")
PORT = os.getenv("PORT")
USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASS")
DATABASE_NAME = os.getenv("DATABASE_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")

# Extract the data from the CSV file into a DataFrame
df = pd.read_csv(r'src\data\logistics_data.csv', parse_dates=["delivery_date"], low_memory=False)
df = df.where(pd.notnull(df), None)
# Establish the database connection
conn = mysql.connector.connect(
    host=HOSTNAME,
    port=PORT,
    user=USERNAME,
    password=PASSWORD )

def update_database(conn, df):
    # Get columns from the dataFrame
    cols = df.columns.tolist()
    # Get data in tuple format from the dataFrame
    data = [tuple(row) for row in df.itertuples(index=False, name=None)]
    # Placeholders for the SQL query
    placeholders = ', '.join(['%s'] * len(cols))

    # SQL query to insert data into the table
    insert_csv_sql = f"INSERT INTO {DATABASE_NAME}.{TABLE_NAME} ({', '.join(cols)}) VALUES ({placeholders})"
    
    try:
        cur= conn.cursor()
        # Execute the insert query for all data
        cur.executemany(insert_csv_sql, data)
        # Saves changes to the database
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

update_database(conn, df)

