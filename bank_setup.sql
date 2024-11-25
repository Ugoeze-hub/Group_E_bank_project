CREATE DATABASE IF NOT EXISTS registered_users;
 USE registered_users;
 CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    User_Name VARCHAR(255),
    Date_of_Birth VARCHAR(255)
    Phone_Number INT,
    National_Identification_Number VARCHAR(11),
    Email VARCHAR(255),
    Pass_word VARCHAR(255),
    Account_Type TEXT

 );