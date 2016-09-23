CREATE TABLE IF NOT EXISTS members (
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

CREATE TABLE IF NOT EXISTS households (
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

CREATE TABLE IF NOT EXISTS districts (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT,
    districtLeaderId INTEGER,
    auxiliaryId INTEGER,
    districtLeaderIndividualId INTEGER
);

CREATE TABLE IF NOT EXISTS companionships (
    id INTEGER PRIMARY KEY NOT NULL,
    startDate INTEGER,
    districtId INTEGER
);

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY NOT NULL,
    individualId INTEGER,
    companionshipId INTEGER
);

CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY NOT NULL,
    assignmentId INTEGER,
    month INTEGER,
    year INTEGER,
    visited BOOLEAN
);

CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY NOT NULL,
    companionshipId INTEGER,
    individualId INTEGER,
    assignmentType TEXT
);

CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY NOT NULL,
            positionTypeName TEXT,
            orgTypeName TEXT,
            positionTypeId INTEGER,
            individualId INTEGER,
            orgId INTEGER,
            orgTypeId INTEGER
);

CREATE VIEW IF NOT EXISTS teacherInfo AS
  SELECT * FROM teachers INNER JOIN members
    WHERE members.individualId=teachers.individualId;

CREATE VIEW IF NOT EXISTS assignmentInfo AS
  SELECT * FROM assignments INNER JOIN members
    WHERE assignments.individualId=members.individualId;

CREATE VIEW IF NOT EXISTS positionInfo AS
  SELECT * FROM positions INNER JOIN members
    WHERE positions.individualId=members.individualId;

CREATE VIEW IF NOT EXISTS districtInfo AS
  SELECT * FROM districts INNER JOIN positionInfo
    WHERE districtLeaderId=positionInfo.id;

CREATE VIEW IF NOT EXISTS companionInfo AS
  SELECT * FROM teacherInfo INNER JOIN companionships
    WHERE teacherInfo.companionshipId=companionships.id;

CREATE VIEW IF NOT EXISTS companionshipInfo AS
  SELECT * FROM companionInfo INNER JOIN districts
    WHERE companionInfo.districtId=districts.id;

CREATE VIEW IF NOT EXISTS memberInfo AS
  SELECT * FROM households INNER JOIN members
    WHERE members.headOfHouseIndividualId=households.headOfHouseIndividualId;

CREATE VIEW IF NOT EXISTS unassignedHouseholds AS
  SELECT * FROM households
    WHERE NOT EXISTS
      (SELECT 1 FROM assignments
         WHERE assignments.individualId=headOfHouseIndividualId);

CREATE VIEW IF NOT EXISTS teacherAssignments AS
  SELECT teachers.individualId, assignments.id AS assignmentId
    FROM teachers INNER JOIN assignments
      WHERE teachers.companionshipId=assignments.companionshipId;

CREATE VIEW IF NOT EXISTS teacherVisits AS
  SELECT teacherAssignments.individualId, visits.*
    FROM visits INNER JOIN teacherAssignments
      WHERE visits.assignmentId=teacherAssignments.assignmentId;


-- Local Variables:
-- mode: sql
-- sql-product: sqlite
-- End:
