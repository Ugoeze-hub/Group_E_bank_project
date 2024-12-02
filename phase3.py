import mysql.connector
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import csv

app = Flask(__name__, template_folder='.')

# Helper function for establishing DB connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='GroupE_YDF',  
        password='GroupE_TUMA',
        database='registered_users'  
    )

# # Function to upload CSV to MySQL (if needed)
# def upload_csv_to_mysql(csv_file_path):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     with open(csv_file_path, newline='', encoding='utf-8') as f:
#         reader = csv.reader(f)
#         next(reader)  # Skip header
#         for row in reader:
#             cursor.execute(
#                 "INSERT INTO registered_users (Username, Date_of_Birth, Phone_Number, National_Identification_Number_(NIN), Email, Password, Pin, Account_Type) "
#                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#                 row
#             )

#     conn.commit()
#     cursor.close()
#     conn.close()
    
@app.route('/')
def home():
    return render_template('bank_homepage.html')

# Refactored Bank Registration method with password hashing
@app.route("/signup", methods=["GET", "POST"])
def signup():
    try:
        if request.method == 'POST':
            # Getting form data
            uname = request.form["User_Name"]
            DOB = request.form["Date_of_Birth"]
            Pnumber = request.form["Phone_Number"]
            NIN = request.form["National_Identification_Number"]
            email = request.form["Email"]
            password = request.form["Password"]
            pin = request.form["Pin"]
            Type_Of_Account = request.form["Account_Type"]

            # Hashing password and pin before storing
            hashed_password = generate_password_hash(password)
            hashed_pin = generate_password_hash(pin)

            # Database connection and query execution
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
            "INSERT INTO users (User_Name, Date_of_Birth, Phone_Number, National_Identification_Number, Email, Pass_word, Pin, Account_Type) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (uname, DOB, Pnumber, NIN, email, hashed_password, hashed_pin, Type_Of_Account)
)


            conn.commit()
            cursor.close()
            conn.close()

            # # If CSV upload is required, call the CSV upload function here
            # upload_csv_to_mysql('path_to_your_csv_file.csv')
            
            return redirect(url_for('main_menu'))

        return render_template("bank_frontend.html")
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return f"There was an issue with the database: {e}", 500
    except Exception as e:
        print(f"General error: {e}")
        return f"Something went wrong: {e}", 500

# Refactored Login method with password validation
@app.route('/login', methods=["GET", "POST"])
def Login():
    try:
        if request.method == 'POST':
            email = request.form["Email"]
            password = request.form["Password"]

            # Database connection and query execution
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            # Check if user exists and password is correct
            if user and check_password_hash(user['Password'], password):
                return redirect(url_for('main_menu'))  # Redirect to menu page 
            else:
                return "Incorrect email or password", 401
            
        return render_template('bank_frontend.html')

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return f"There was an issue with the database: {e}", 500
    except Exception as e:
        print(f"General error: {e}")
        return f"Something went wrong: {e}", 500
    
    
@app.route('/menu', methods=['GET', 'POST'])
def main_menu():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return redirect(url_for('Financial_Services'))
        if choice == '2':
            return redirect(url_for('Customer_Care'))
        if choice == '3':
            return redirect(url_for('Other_Services'))
        if choice == '4':
            return redirect(url_for('home'))
            
    return render_template('bank_menupage.html')

@app.route('/financial_services', methods=['GET', 'POST'])
def Financial_Services():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return redirect(url_for('Transfer'))
        if choice == '2':
            return redirect(url_for('Balance'))
        if choice == '3':
            return redirect(url_for('Account details'))
        if choice == '4':
            return redirect(url_for('main_menu'))
            
    return render_template('bank_financialservices.html')

if __name__ == "__main__":
    app.run(debug=True)
