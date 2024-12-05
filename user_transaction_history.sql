CREATE DATABASE IF NOT EXISTS registered_users;

USE registered_users;

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    User_email VARCHAR(255) NOT NULL,
    Transaction_type VARCHAR(50) NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    Status_ VARCHAR(50) NOT NULL,
    Transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_email) REFERENCES users(Email) ON DELETE CASCADE
);
