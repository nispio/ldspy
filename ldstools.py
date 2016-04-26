#!/usr/bin/python

import requests
import getpass
import json
import sys

# Info about the LDS Tools Web API can be found at:
#   http://tech.lds.org/wiki/LDS_Tools_Web_Services

class LDSTools(object):
    HTVT = {
        "currentUser": "https://www.lds.org/htvt/services/v1/user/currentUser",
        "members": "https://www.lds.org/htvt/services/v1/{unit}/members",
        "memberTags": "https://www.lds.org/htvt/services/v1/{unit}/members/tags",
        "districts": "https://www.lds.org/htvt/services/v1/{unit}/districts/{org}",
        "assignment": "https://www.lds.org/htvt/services/v1/{unit}/assignment/{org}",
        "summaryStats": "https://www.lds.org/htvt/services/v1/{unit}/unit/summaryStats",
        "positions": "https://www.lds.org/htvt/services/v1/{unit}/auxiliaries/positions",
        "userStrings": "https://www.lds.org/htvt/services/v1/user/strings/",
    }

    def __init__(self, username=None, password=None):
        super(LDSTools, self).__init__()
        self.session = requests.session()
        self._username = username
        self._api = None
        self._user_detail = None
        self._current_user = None
        self._members_and_callings = None
        self._members_htvt = None
        self._organization = None
        if username and password:
            self.authenticate(username, password)

    def sign_in(self):
        self._username = self._username or raw_input("username: ")
        password = getpass.getpass("password: ")
        self.authenticate(self._username, password)
        print 'Successfully signed in as "%s"' % (self.currentUser['formattedName'],)
        
        
    def authenticate(self, username, password):
        credentials = {'username' : username, 'password' : password}
        self.session.post(self.api['auth-url'], data=credentials)
        # TODO: Add a check to validate that authentication was successful
        self.__authenticated = True
        return self

    def getjson(self, url, *args, **kwargs):
        return json.loads(self.session.get(url, *args, **kwargs).text)

    @property
    def api(self):
        if self._api is None:
            self._api = self.getjson('https://tech.lds.org/mobile/ldstools/config.json')

        return self._api

    @property
    def userDetail(self):
        if not self.__authenticated:
            raise RuntimeError('Must sign in before accessing online data!')
        
        if self._user_detail is None:
            self._user_detail = self.getjson(self.api['current-user-detail'])

        return self._user_detail


    @property
    def organization(self):
        if self._organization is None:
            currentUser = self.getjson(self.HTVT['currentUser'])
            for org in currentUser['userOrgRights']:
                if org['editable']:
                    self._organization = org['id']

        return self._organization
            

    @property
    def unitNumber(self):
        return self.userDetail['homeUnitNbr']


    @property
    def unitMembersAndCallings(self):
        if self._members_and_callings is None:
            unit = str(self.unitNumber)
            url = self.api['unit-members-and-callings-v2'].replace('%@', unit)
            self._members_and_callings = self.getjson(url)

        return self._members_and_callings

    @property
    def households(self):
        if self._members_htvt is None:
            unitNumber = str(self.unitNumber)
            url = self.HTVT['members'].format(unit=unitNumber)
            self._members_htvt = self.getjson(url)['families']

        return self._members_htvt

    @property
    def directory(self):
        return self.unitMembersAndCallings['households']
    
    @property
    def callings(self):
        return self.unitMembersAndCallings['callings']

    @property
    def name(self):
        return self.unitMembersAndCallings['orgName']

    @property
    def currentUser(self):
        if self._current_user == None:
            individualId = self.userDetail['individualId']
            self._current_user = self.findIndividual(individualId)

        return self._current_user

    def findIndividualAndHouse(self, individualId):
        blank = {'individualId': -1}
        for house in self.households:
            headOfHouse = house.get('headOfHouse', blank)
            spouse = house.get('spouse', blank) or blank
            if individualId == headOfHouse['individualId']:
                return headOfHouse, house
            elif individualId == spouse['individualId']:
                return spouse, house
            else:
                for child in house.get('children', []):
                    if individualId == child['individualId']:
                        return child, house

        else:
            return blank, blank

    def findIndividual(self, individualId):
        return self.findIndividualAndHouse(individualId)[0]

    def findHousehold(self, individualId):
        return self.findIndividualAndHouse(individualId)[1]


if __name__=='__main__':
    ward = LDSTools()
    ward.sign_in()

    print 'Downloaded info for unit: %s - %d' % (ward.name, ward.unitNumber)
