CREATE TABLE User (
    user_id VARCHAR(20) PRIMARY KEY,
    password VARCHAR(20) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    email VARCHAR(50),
    acct_creation_date DATE NOT NULL
);

CREATE TABLE Income (
    amount FLOAT NOT NULL,
    user_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE Category (
    name VARCHAR(20) NOT NULL,
    description VARCHAR(100)
);

CREATE TABLE Expense (
    name VARCHAR(20) NOT NULL,
    description VARCHAR(100),
    amount FLOAT NOT NULL,
    category Category NOT NULL,
    date_purchased DATE NOT NULL,
    user_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
    ON UPDATE CASCADE 
    ON DELETE CASCADE
);

CREATE TABLE Budget (
    amount FLOAT,
    category Category,
    month VARCHAR(10),
    year INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
    ON UPDATE SET NULL
    ON DELETE SET NULL
);
