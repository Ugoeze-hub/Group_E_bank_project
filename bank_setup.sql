CREATE DATABASE IF NOT EXISTS registered_users;

USE registered_users;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    User_Name VARCHAR(255),
    Date_of_Birth DATE,  -- Changed to DATE to store date properly
    Phone_Number VARCHAR(15),  -- Changed to VARCHAR to store phone number with country code
    National_Identification_Number VARCHAR(20),  -- Changed length to 20 to accommodate longer NIN formats
    Email VARCHAR(255) UNIQUE,  -- Added UNIQUE constraint for email
    Pass_word VARCHAR(255),  -- Corrected column name for password
    Pin VARCHAR(255),  -- Changed Pin to VARCHAR to match the hashed format
    Account_Type VARCHAR(50)  -- Changed to VARCHAR to limit account type length
);