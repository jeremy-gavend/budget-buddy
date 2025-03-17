# Launch only once to create a local database!!
CREATE DATABASE budget_buddy;
USE budget_buddy;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL
);

CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    balance DECIMAL(10, 2) NOT NULL,
    user_id BIGINT UNSIGNED,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

# Alternative: Create a new table when a new user is created; reuse a table with foreign key associated with user
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    type VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);