import pandas as pd
import mysql.connector
# MySQL connection details
db_config = {
    'user': 'GroupE_YDF',
    'password': 'GroupE_TUMA',
    'host': 'localhost',
    'database': 'registered_users'
}


def upload_csv_to_mysql(csv_file, table_name):
    # Read CSV file
    data = pd.read_csv(csv_file)
    
    # Establish a database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # Insert data into MySQL table
    

    for _, row in data.iterrows():
        cursor.execute(
            f"INSERT INTO {table_name} (id, name, age, email) VALUES (%s, %s, %s, %s)",
            (row['id'], row['name'], row['age'], row['email'])
        )
    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Data uploaded successfully")
# Upload data from CSV to MySQL
upload_csv_to_mysql('data.csv', 'users')