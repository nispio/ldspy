#!/usr/bin/python

import requests
import getpass
import json
import sys

# Info about the LDS Tools Web API can be found at:
#   http://tech.lds.org/wiki/LDS_Tools_Web_Services

class LDSTools(object):
    def __init__(self, username=None, password=None):
        super(LDSTools, self).__init__()
        self.session = requests.session()
        self._username = username
        self._api = None
        self._user_detail = None
        self._current_user = None
        self._members_and_callings = None
        if username and password:
            self._authenticate(username, password)

    def sign_in(self):
        self._username = self._username or raw_input("username: ")
        password = getpass.getpass("password: ")
        self._authenticate(self._username, password)
        print 'Successfully signed in as "%s"' % (self.currentUser['preferredName'],)
        
        
    def _authenticate(self, username, password):
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


    def findIndividual(self, individualId):
        blank = {'individualId': -1}
        for house in self.households:
            headOfHouse = house.get('headOfHouse', blank)
            spouse = house.get('spouse', blank)
            if individualId == headOfHouse['individualId']:
                return headOfHouse
            elif individualId == spouse['individualId']:
                return spouse
            else:
                for child in house.get('children', []):
                    if individualId == child['individualId']:
                        return child


if __name__=='__main__':
    ward = LDSTools()
    ward.sign_in()

    print 'Downloaded info for unit: %s - %d' % (ward.name, ward.unitNumber)
