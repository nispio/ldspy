
import sqlite3
import os

from sqldict import SqlTable

HTVT_DB_PATH = "data/htvt.db"
HTVT_DB_SCHEMA = "htvt.sql"

class HomeTeachingDB(object):
    def __init__(self, db=HTVT_DB_PATH, schema=HTVT_DB_SCHEMA):
        self._initialized = os.path.exists(db)
        self._path = db
        self._conn = sqlite3.connect(db)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor

        self._schema_path = schema
        self.initSchema(schema)

        self._households = HouseholdsTable(self._conn)
        self._members = MembersTable(self._conn)
        self._districts = DistrictsTable(self._conn)
        self._companionships = CompanionshipsTable(self._conn)
        self._teachers = TeachersTable(self._conn)
        self._assignments = AssignmentsTable(self._conn)
        self._visits = VisitsTable(self._conn)

    def initSchema(self, schema_path):
        if self._initialized:
            return

        with open(schema_path, 'r') as schema_file:
            schema = schema_file.read()

        with self._conn as db:
            db.executescript(schema)

        self._initialized = True


    def updateHouseholds(self, households):
        if "families" in households:
            households = households["families"]

        self._households.insertmany(households)

        members = []
        for house in households:
            headOfHouse = house['headOfHouse']
            members.append(headOfHouse)
            spouse = house.get('spouse')
            if spouse:
                members.append(spouse)
            for child in house.get('children', []):
                members.append(child)

        self._members.insertmany(members)


    def updateDistricts(self, districts):
        self._districts.insertmany(districts)

        companionships = []
        teachers = []
        assignments = []
        visits = []
        for district in districts:
            for companionship in district['companionships']:
                companionships.append(companionship)
                for teacher in companionship['teachers']:
                    teachers.append(teacher)
                for assignment in companionship['assignments']:
                    assignments.append(assignment)
                    for visit in assignment['visits']:
                        visits.append(visit)

        self._companionships.insertmany(companionships)
        self._teachers.insertmany(teachers)
        self._assignments.insertmany(assignments)
        self._visits.insertmany(visits)


    def __call__(self, sql, args=None):
        with self._conn as db:
            if args is None:
                db.execute(sql)
            elif isinstance(args, tuple):
                db.execute(sql, args)
            else:
                db.executemany(sql, args)

            return db.fetchone()


class DistrictsTable(SqlTable):
    def __init__(self, db, **kwargs):
        keys = (
            "id",
            "name",
            "districtLeaderId",
            "auxiliaryId",
            "districtLeaderIndividualId",
        )
        super(DistrictsTable, self).__init__(db, table="districts", keys=keys, **kwargs)


class CompanionshipsTable(SqlTable):
    def __init__(self, db, **kwargs):
        keys = (
            "id",
            "startDate",
            "districtId",
        )
        super(CompanionshipsTable, self).__init__(db, table="companionships", keys=keys, **kwargs)


class TeachersTable(SqlTable):
    def __init__(self, db, **kwargs):
        keys = (
            "id",
            "individualId",
            "companionshipId",
        )
        super(TeachersTable, self).__init__(db, table="teachers", keys=keys, **kwargs)


class VisitsTable(SqlTable):
    def __init__(self, db, **kwargs):
        keys = (
            "id",
            "assignmentId",
            "month",
            "year",
            "visited",
        )
        super(VisitsTable, self).__init__(db, table="visits", keys=keys, **kwargs)


class AssignmentsTable(SqlTable):
    def __init__(self, db, **kwargs):
        keys = (
            "id",
            "companionshipId",
            "individualId",
            "assignmentType",
        )
        super(AssignmentsTable, self).__init__(db, table="assignments", keys=keys, **kwargs)


class MembersTable(SqlTable):
    def __init__(self, db, **kwargs):
        keys = (
            "individualId",
            "formattedName",
            "surname",
            "gender",
            "priesthoodOffice",
            "givenName1",
            "phone",
            "birthdate",
            "headOfHouseIndividualId",
            "email",
            "isAdult",
            "teacherAuxIds/htAuxiliaries/0",
        )
        super(MembersTable, self).__init__(db, table="members", keys=keys, **kwargs)


class HouseholdsTable(SqlTable):
    def __init__(self, db, **kwargs):
        keys = (
            'headOfHouse/headOfHouseIndividualId',
            'formattedCoupleName',
            'isAssignedHT',
            'responsibleHTAuxiliaryId',
            'phone',
            'emailAddress',
            'address/streetAddress',
            'address/streetAddress2',
            'address/city',
            'address/state',
            'address/postal',
        )
        super(HouseholdsTable, self).__init__(db, table="households", keys=keys, **kwargs)
