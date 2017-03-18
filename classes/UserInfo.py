import json, inspect

#stores user info
class UserInfo(object):
    def __init__(self, name, id):
        self.name = str(name)
        self.ID = str(id)

    def __str__(self):
        return str(self.__dict__)