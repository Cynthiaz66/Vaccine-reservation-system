CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);
CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers(Username),
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Dose int,
    PRIMARY KEY (Name)
);

CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16), 
    PRIMARY KEY(Username)
);

CREATE TABLE Appointments (
    ID VARCHAR(255),
    cname VARCHAR(255) REFERENCES Caregivers(Username),
    pname VARCHAR(255) REFERENCES Patients(Username),
    vname VARCHAR(255) REFERENCES Vaccines(Name),
    Time DATE ,
    PRIMARY KEY(ID)
);
