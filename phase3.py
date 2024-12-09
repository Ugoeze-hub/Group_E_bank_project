import mysql.connector
from flask import Flask, request, session, flash, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from decimal import Decimal
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
        print(f"Choice received: {choice}")  # Debugging line

        if choice == '1':
            print("Redirecting to Transfer_Funds")  # Debugging line
            return redirect(url_for('Transfer_Funds'))
        elif choice == '2':
            print("Redirecting to Deposit_Funds")  # Debugging line
            return redirect(url_for('Deposit_Funds'))
        elif choice == '3':
            return redirect(url_for('Balance'))
        elif choice == '4':
            return redirect(url_for('Transaction_History'))
        elif choice == '5':
            return redirect(url_for('main_menu'))
    return render_template('bank_financialservices.html')



@app.route('/transfer', methods = ['GET', 'POST'])
def Transfer_Funds():
    if request.method == 'POST':
        recipient_account = request.form["recipient_account"]
        recipient_bank = request.form["recipient_bank"]
        recipient_name = request.form["recipient_name"]
        
        # Store recipient details in the session
        session['recipient_account'] = recipient_account
        session['recipient_bank'] = recipient_bank
        session['recipient_name'] = recipient_name

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE Email = %s", (session.get('Email'),))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        return redirect(url_for('Transfer_Pin'))
        
    return render_template('bank_transfer.html')

@app.route('/transfer_pin', methods=['GET', 'POST'])
def Transfer_Pin():
    if request.method == 'POST':
        # Get data from the form
        sender_pin = request.form['sender_pin']
        amount = Decimal(request.form['amount'])

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
        
        # # Fetch recipient data from session
        # recipient_account = session.get('recipient_account')
        # recipient_bank = session.get('recipient_bank')
        # recipient_name = session.get('recipient_name')

        # Update balances
        new_sender_balance = sender['Balance'] - amount

        cursor.execute("UPDATE users SET Balance = %s WHERE Email = %s", (new_sender_balance, session.get('Email')))

        # Insert transaction into the transaction history
        cursor.execute(
            "INSERT INTO transactions (user_email, transaction_type, amount, Status_) VALUES (%s, %s, %s, %s)",
            (session.get('Email'), 'transfer', amount, 'success')
        )
    

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f'The amount of {amount} has been transfered to your account. New balance is {new_sender_balance}')
        return redirect(url_for('main_menu'))  # Redirect back to the main menu

    return render_template('bank_transferpin.html')

        
@app.route('/deposit', methods = ['GET', 'POST'])
def Deposit_Funds():
    if request.method == 'POST':
        password = request.form["password"]
        
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE Email = %s", (session.get('Email'),))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['Pass_word'], password):  # Validate password
            # Proceed with the transfer process
            return redirect(url_for('Deposit_pin'))
        else:
            return "Invalid password", 401

    return render_template('bank_deposit.html')
        
@app.route('/deposit_pin', methods = ['GET', 'POST'])
def Deposit_pin():
    if request.method == 'POST':
        pin = request.form["pin"]
        amount = Decimal(request.form['amount'])
        
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE Email = %s", (session.get('Email'),))
        user = cursor.fetchone()
    

        if user and check_password_hash(user['Pin'], pin): # Validate password
            cursor.execute("SHOW COLUMNS FROM users LIKE 'Balance'")
            balance_column = cursor.fetchone()

            # If 'Balance' column doesn't exist, add it
            if not balance_column:
                cursor.execute("ALTER TABLE users ADD COLUMN Balance DECIMAL(10, 2) DEFAULT 0.00")
                conn.commit()  
                
                cursor.execute("SELECT * FROM users WHERE Email = %s", (session.get('Email'),))
                user = cursor.fetchone()
            
            new_balance = user['Balance'] + amount
            
            cursor.execute("UPDATE users SET Balance = %s WHERE Email = %s", (new_balance, session.get('Email')))
            
            cursor.execute(
                "INSERT INTO transactions (user_email, transaction_type, amount, Status_) "
                "VALUES (%s, %s, %s, %s)",
                (session.get('Email'), 'deposit', amount, 'success')
            )
            
            conn.commit()          
            
            cursor.close()
            conn.close()
            # Proceed with the transfer process
            print(f'The amount of {amount} has been deposited in your account. New balance is {new_balance}')
            return redirect(url_for('main_menu'))
        else:
            cursor.close()
            conn.close()
            return "Invalid password", 401
        
    return render_template('bank_depositpin.html')    


        
@app.route('/transaction_history', methods=['GET'])
def transaction_History():
    user_email = session.get('Email')
    
    if not user_email:
        return redirect(url_for('Login'))  # Redirect to login if the user is not logged in

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch transaction history for the logged-in user
    cursor.execute("SELECT * FROM transactions WHERE user_email = %s", (user_email,))
    transactions = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('transaction_history.html', transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)
