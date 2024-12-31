# SPARK Bank Application

 SPARK Bank is a simulation banking application built using HTML, CSS, JavaScript, Python, Flask and MySQL and other tools like werkzeug.security for secure password management.
 It allows users to register an account, login and perform various banking functions

# Features

### It includes features such as:
* User Registration: Registers users and securely hashes their passwords and PINs.
  
* User Login: Allows users to log in with email and password, verifying credentials securely.
  
* Main Menu: Displays a main menu with options to access financial services, customer care, and other services.
  
* Financial Services: Includes features like:
  
     * Fund Transfer: Validates the PIN, checks balance, and updates the user's balance.
       
     * Deposit Funds: Validates PIN and updates the user's balance accordingly.
       
     * and more...
 
# Highlights:

* Database Integration: Uses MySQL for storing user and transaction data.
  
* Password and PIN Hashing: Ensures secure storage of sensitive data.
  
* Session Management: Maintains user sessions for secure interaction.
  
* Error Handling: Includes error handling for database and general exceptions.
  
* Flash Messages: Provides user feedback for successful or failed operations.

# Requirements

* Python 3.x
  
* Flask (usually included with Python)

* MySQL (WampServer Recommended)

* Anaconda (optional, for managing dependencies)

* Any IDE of your choice

# Installation

1. Clone the Repository

```
git clone https://github.com/Ugoeze-hub/SPARK-Bank-Simulation)
cd SPARK-Bank-Simulation
```

Create a virtual environment (Optional):

```
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

Install required packages:

```
pip install -r requirements.txt
```

# Usage

## Create a new database and replace this details eith yours:

```
app.secret_key = 'groupE'
```

```
host='localhost',
user='GroupE_YDF',  
password='GroupE_TUMA',
database='registered_users'  
```

## Run the application:

```
phase3.py
```

Follow the on-screen instructions to sign up or log in.

# Project Structure

* phase3.py: Contains the main application logic and user management logic, including signup and login functions.

* Files with the .html extension: Contains the application frontend code which encompasses the usage of HTML, CSS and JavaScript languages

* Files with the .sql extension: Contains the setup format used to create the databases

# Acknowledgements

* Python
  
* Wampserver

* Flask

* HTML

* CSS

* JavaScript

* [Yomi Denzel Foundation](https://yomidenzelfoundation.org.ng)


