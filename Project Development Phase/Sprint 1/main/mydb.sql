DROP TABLE IF EXISTS users;
CREATE TABLE users (
    uname TEXT NOT NULL,
    DOB DATE NOT NULL,
    Mobile INTEGER NOT NULL,
    email TEXT NOT NULL PRIMARY KEY,
    uaddress TEXT,
    city TEXT NOT NULL,
    pincode INTEGER NOT NULL,
    pass TEXT NOT NULL,
    joined TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);