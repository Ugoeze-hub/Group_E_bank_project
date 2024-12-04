CREATE DATABASE IF NOT EXISTS registered_users;

USE users_transaction;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    User_Name VARCHAR(255),
    Date_of_Birth DATE,
    Phone_Number VARCHAR(15),  
    National_Identification_Number VARCHAR(20), 
    Email VARCHAR(255) UNIQUE,
    Pass_word VARCHAR(255), 
    Pin VARCHAR(255),  
    Account_Type VARCHAR(50)  
);