from flask import Flask, request, render_template, redirect, url_for
import os
import csv
import mysql.connector
import pandas as pd

app = Flask(__name__)
class Bank_functions():
    def __init__(self, name):
        self.name = 'UPAY'
    

    def Bank_registeration(self, uname, DOB, Pnumber, NIN, email, Password, Type_Of_Account):
        registration_data = [
            {'Username': uname, 'Date_of_Birth' : DOB, 'Phone_Number' : Pnumber, 'National_Identification_Number_(NIN)' : NIN, 'Email' : email, 'Password' : Password, 'Account_Type' : Type_Of_Account}
        ]

        fieldnames = ["Username", "Date_of_Birth", "Phone_Number", "National_Identification_Number_(NIN)", "Email", "Password", "Account_Type"]

        # Check if the file exists and is empty or not
        file_exists = os.path.isfile(f'Registrered {self.name} Users.csv') and os.path.getsize(f'Registrered {self.name} Users.csv') > 0

        # Open the CSV file in append mode
        with open(f'Registrered {self.name} Users.csv', 'a') as registrar:
            writer = csv.DictWriter(registrar, fieldnames=fieldnames)
    
        # Write the header only if the file is empty
        if not file_exists:
            writer.writeheader()  # Write the header row
        
        # Write the new data rows
        writer.writerows(registration_data)
        
        # try:
        #     # Upload data from CSV to MySQL
        #     upload_csv_to_mysql(f'Registrered {self.name} Users.csv', 'registered_users')
        # except Exception as e:
        #     print(f"Error uploading data to MySQL: {e}")

        def upload_csv_to_mysql(csv_file, table_name):
            # Read CSV file
            db_config = {
            'user': 'GroupE_YDF',
            'password': 'GroupE_TUMA',
            'host': 'localhost',
            'database': 'registered_users'
    }
            data = pd.read_csv(csv_file)
            
            # Establish a database connection
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            # Insert data into MySQL table
            

            for _, row in data.iterrows():
                cursor.execute(
                    f"INSERT INTO {table_name} (Username, Date_of_Birth, Phone_Number, National_Identification_Number_(NIN), Email, Password, Account_Type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    ( row['Username'], row['Date_of_Birth'], row['Phone_Number'], row['National_Identification_Number_(NIN)'], row['Email'], row['Password'], row['Account_Type'])
                )
            # Commit and close the connection
            conn.commit()
            cursor.close()
            conn.close()
            print("Data uploaded successfully")
        # Upload data from CSV to MySQL
        upload_csv_to_mysql(f'Registrered {self.name} Users.csv', 'registered_users')
        
        
@app.route('/')
def home():
    return render_template('bank_frontend.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Username = request.form['uname']
        Date_of_Birth = request.form['DOB']
        Phone_Number = request.form['Pnumber']
        National_Identification_Number = request.form['NIN']
        Email = request.form['email']
        password = request.form['password']
        Account_Type = request.form['Type_Of_Account']

        bank = Bank_functions('UPAY')
        bank.Bank_registeration(Username, Date_of_Birth, Phone_Number, National_Identification_Number, Email, password, Account_Type)

        return redirect(url_for('home'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
        