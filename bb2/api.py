"""BB2 api agent modul"""
import requests

class Agent:
    """BB2 api agent"""
    BASE_URL = "http://web.cyanide-studio.com/ws/bb2/"
    def __init__(self, api_key):
        self.api_key = api_key

    def team(self, name):
        """Pulls team data"""
        r = self.call("team", name=name)
        data = r.json()
        return data

    def match(self, id):
        """Pulls match id data"""
        r = self.call("match", match_id=id)
        data = r.json()
        return data

    def league(self, name):
        """Pulls league data"""
        r = self.call("league", league=name)
        data = r.json()
        return data

    def matches(self, **kwargs):
        """Pull matches"""
        if 'limit' not in kwargs:
            kwargs['limit'] = 10000
        if 'v' not in kwargs:
            kwargs['v'] = 1
        if 'exact' not in kwargs:
            kwargs['exact'] = 0
        if 'start' not in kwargs:
            kwargs['start'] = '2016-01-01'
        if 'league' not in kwargs:
            kwargs['league'] = 'REBBL Imperium,REBBL Imperium Extra,REBBL Imperium Extra 2'
        r = self.call("matches", **kwargs)
        data = r.json()
        return data

    def contests(self, **kwargs):
        """Pull matches"""
        if 'limit' not in kwargs:
            kwargs['limit'] = 10000
        if 'status' not in kwargs:
            kwargs['status'] = 'played'
        if 'league' not in kwargs:
            kwargs['league'] = 'REBBL Imperium,REBBL Imperium Extra,REBBL Imperium Extra 2'
        r = self.call("contests", **kwargs)
        data = r.json()
        return data

    def call(self, method, **kwargs):
        """Call the api method with kwargs parameters"""
        url = self.__class__.BASE_URL + method+"/"
        kwargs['key'] = self.api_key
        kwargs['order'] = 'CreationDate'
        return requests.get(url=url, params=kwargs)
