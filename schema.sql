DROP TABLE IF EXISTS donors;
DROP TABLE IF EXISTS volunteers;

CREATE TABLE donors (
    email VARCHAR(256) PRIMARY KEY,
    password VARCHAR(1024),
    phone VARCHAR(12)
);


CREATE TABLE volunteers (
    email VARCHAR(256) PRIMARY KEY,
    password VARCHAR(1024),
    phone VARCHAR(12)
);