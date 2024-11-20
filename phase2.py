import os
import csv

class Bank_functions():
    def __init__(self, name):
        self.name = 'TUMA'
    

    def Bank_registeration(self, uname, email, Pnumber, BVN, Type_Of_Account):
        registration_data = [
            {'Username': uname, 'Email' : email, 'Phone_Number' : Pnumber, 'BVN_autogenerate' : BVN, 'Account_Type' : Type_Of_Account}
        ]

        fieldnames = ["Username", "Email", "Phone_Number", "BVN_autogenerate", "Account_Type"]

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
        