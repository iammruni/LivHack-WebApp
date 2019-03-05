
DROP TABLE IF EXISTS users_cus;
DROP TABLE IF EXISTS users_des;


CREATE TABLE users_cus(
    id INTEGER PRIMARY KEY ,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE users_des(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL 
);






