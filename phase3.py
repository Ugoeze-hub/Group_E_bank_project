import mysql.connector
from flask import Flask, request, session, flash, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import csv

app = Flask(__name__, template_folder='.')
app.secret_key = 'groupE'

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
            if user and check_password_hash(user['Pass_word'], password):
                session['Email'] = email
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
    # except mysql.connector.Error as e:
    #     flash(f"Database error: {e}", "danger")
    #     return redirect(url_for('Login'))
    # except Exception as e:
    #     flash(f"Something went wrong: {e}", "danger")
    #     return redirect(url_for('Login'))
    
@app.route('/menu', methods=['GET', 'POST'])
def main_menu():
    user_email = session.get('Email')

    # if not user_email:
    #     return redirect(url_for('Login'))  # Redirect to login if the user is not logged in

    # Fetch the user's details from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT User_Name FROM users WHERE Email = %s", (user_email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        username = user['User_Name']
    else:
        username = "Guest"  # If no user is found, use a default value
        
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
            
    return render_template('bank_menupage.html', uname=username)

@app.route('/financial_services', methods=['GET', 'POST'])
def Financial_Services():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return redirect(url_for('Transfer_Funds'))
        if choice == '2':
            return redirect(url_for('Balance'))
        if choice == '3':
            return redirect(url_for('Account details'))
        if choice == '4':
            return redirect(url_for('main_menu'))
            
    return render_template('bank_financialservices.html')

@app.route('/transfer', methods = ['GET', 'POST'])
def Transfer_Funds():
    if request.method == 'POST':
        password = request.form["sender_password"]
        recipient_account = request.form["recipient_account"]
        recipient_bank = request.form["recipient_bank"]
        recipient_name = request.form["recipient_name"]
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE Email = %s", (session.get('Email'),))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['Pass_word'], password):  # Validate password
            # Proceed with the transfer process
            return redirect(url_for('Transfer_Pin'))
        else:
            return "Invalid password", 401
    return render_template('bank_transfer.html')

@app.route('/transfer_pin', methods=['GET', 'POST'])
def Transfer_Pin():
    if request.method == 'POST':
        # Get data from the form
        sender_pin = request.form['sender_pin']
        amount = float(request.form['amount'])

        # Fetch the sender's data from the session (i.e., the logged-in user)
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE Email = %s", (session.get('Email'),))
        sender = cursor.fetchone()

        if not sender:
            return "Sender not found", 404

        # Validate the sender's PIN
        if not check_password_hash(sender['Pin'], sender_pin):
            return "Invalid PIN", 401

        # Check if the sender has enough balance
        if sender['Balance'] < amount:
            return "Insufficient funds", 400

        # Update balances
        new_sender_balance = sender['Balance'] - amount

        cursor.execute("UPDATE users SET Balance = %s WHERE Email = %s", (new_sender_balance, session.get('Email')))

        # Insert transaction into the transaction history
        cursor.execute(
            "INSERT INTO transactions (sender_email, amount) VALUES (%s, %s, %s)",
            (session.get('Email'), amount)
        )

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('main_menu'))  # Redirect back to the main menu

    return render_template('bank_transferpin.html')

        

        
if __name__ == "__main__":
    app.run(debug=True)
