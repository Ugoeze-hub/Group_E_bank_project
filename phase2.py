from flask import Flask, request, render_template, redirect, url_for
import os
import csv
import mysql.connector
import pandas as pd
from werkzeug.security import generate_password_hash

app = Flask(__name__, template_folder='.')
class Bank_functions():
    def __init__(self, name):
        self.name = 'UPAY'
        
    @staticmethod    
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
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            # Database operations
            
            for _, row in data.iterrows():
                cursor.execute(
                    f"INSERT INTO {table_name} (Username, Date_of_Birth, Phone_Number, National_Identification_Number_(NIN), Email, Password, Account_Type, Pin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    ( row['Username'], row['Date_of_Birth'], row['Phone_Number'], row['National_Identification_Number_(NIN)'], row['Email'], row['Password'], row['Account_Type'], row['Pin'])
                )
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
        finally:
            # Commit and close the connection
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("Data uploaded successfully")
                
    # # Upload data from CSV to MySQL
    # upload_csv_to_mysql(f'Registrered {self.name} Users.csv', 'registered_users')
    
        
    

    def Bank_registeration(self, uname, DOB, Pnumber, NIN, email, Password, pin, Type_Of_Account):
        hashed_password = generate_password_hash(Password)
        hashed_pin = generate_password_hash(pin)
        registration_data = [
            {'Username': uname, 'Date_of_Birth' : DOB, 'Phone_Number' : Pnumber, 'National_Identification_Number_(NIN)' : NIN, 'Email' : email, 'Password' : hashed_password, 'Pin' : hashed_pin, 'Account_Type' : Type_Of_Account}
        ]

        fieldnames = ["Username", "Date_of_Birth", "Phone_Number", "National_Identification_Number_(NIN)", "Email", "Password", 'Pin', "Account_Type"]

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
        
        try:
            # Upload data from CSV to MySQL
            self.upload_csv_to_mysql(f'Registrered {self.name} Users.csv', 'registered_users')
        except Exception as e:
            print(f"Error uploading data to MySQL: {e}")


@app.route('/')
def home():
    return render_template('bank_homepage.html')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Username = request.form['uname']
        Date_of_Birth = request.form['DOB']
        Phone_Number = request.form['Pnumber']
        National_Identification_Number = request.form['NIN']
        Email = request.form['email']
        password = request.form['password']
        pin = request.form['pin']
        Account_Type = request.form['Type_Of_Account']

        bank = Bank_functions('UPAY')
        bank.Bank_registeration(Username, Date_of_Birth, Phone_Number, National_Identification_Number, Email, password, pin, Account_Type)

        return redirect(url_for('main_menu'))

    return render_template('bank_frontend.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Email = request.form['email']
        password = request.form['password']

        return redirect(url_for('main_menu'))

    return render_template('bank_frontend.html')

@app.route('/menu', methods=['GET', 'POST'])
def main_menu():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return redirect(url_for('Financial Services.html'))
        if choice == '2':
            return redirect(url_for('Customer Care.html'))
        if choice == '3':
            return redirect(url_for('Other Services.html'))
        if choice == '4':
            return redirect(url_for('home'))
            
        

if __name__ == '__main__':
    app.run(debug=True)
        