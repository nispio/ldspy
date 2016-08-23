
CREATE TABLE members (
    individualId INTEGER PRIMARY KEY NOT NULL,
    headOfHouseIndividualId INTEGER,
    formattedName TEXT,
    surname TEXT,
    givenName1 TEXT,
    gender TEXT,
    priesthoodOffice TEXT,
    phone TEXT,
    email TEXT,
    birthdate TEXT,
    isAdult BOOLEAN,
    htAuxiliaries0 INTEGER
);

CREATE TABLE households (
    headOfHouseIndividualId INTEGER PRIMARY KEY NOT NULL,
    formattedCoupleName TEXT,
    isAssignedHT BOOLEAN,
    responsibleHTAuxiliaryId INTEGER,
    phone TEXT,
    emailAddress TEXT,
    streetAddress TEXT,
    streetAddress2 TEXT,
    city TEXT,
    state TEXT,
    postal TEXT
);

CREATE TABLE districts (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT,
    districtLeaderId INTEGER,
    auxiliaryId INTEGER,
    districtLeaderIndividualId INTEGER
);

CREATE TABLE companionships (
    id INTEGER PRIMARY KEY NOT NULL,
    startDate INTEGER,
    districtId INTEGER
);

CREATE TABLE teachers (
    id INTEGER PRIMARY KEY NOT NULL,
    individualId INTEGER,
    companionshipId INTEGER
);


CREATE TABLE visits (
    id INTEGER PRIMARY KEY NOT NULL,
    assignmentId INTEGER,
    month INTEGER,
    year INTEGER,
    visited BOOLEAN
);

CREATE TABLE assignments (
    id INTEGER PRIMARY KEY NOT NULL,
    companionshipId INTEGER,
    individualId INTEGER,
    assignmentType TEXT
);



-- Local Variables:
-- mode: sql
-- sql-product: sqlite
-- End:
