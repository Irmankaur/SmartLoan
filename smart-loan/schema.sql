CREATE DATABASE IF NOT EXISTS smartloan;
USE smartloan;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    income DECIMAL(15,2) DEFAULT 0,
    expenses DECIMAL(15,2) DEFAULT 0,
    emergency_reserve DECIMAL(15,2) DEFAULT 0
);

CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    loan_type VARCHAR(50),
    principal DECIMAL(15,2),
    interest_rate DECIMAL(5,2),
    tenure_months INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
