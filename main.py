import requests

BASE_URL = 'http://178.128.217.110:8381/'

ACTION = {"create_user": "user", 'authentication': 'authentication', 'search': 'FinalFinalFinalFinalManagerID/elasticsearch',
          'post': 'FinalFinalFinalFinalManagerID/create', 'put': 'FinalFinalFinalFinalManagerID/update', 'get': 'FinalFinalFinalFinalManagerID/get'}

class V_chainAPIs:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        self.header = {'Authorization': 'Bearer {}'.format(self.makeAuthentication())}

    def createUser(self):
        """
        create user with role is manager or citizen
        """
        link = BASE_URL + ACTION["create_user"]
        json = {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }
        r = requests.post(link, json=json)
        return r.json()
    def makeAuthentication(self):
        """
        make authentication token for user's account
        """
        link = BASE_URL + ACTION['authentication']
        json = {
            'username': self.username,
            'password': self.password
        }
        return requests.post(link, json=json).json()['authorization']

    def get(self, cmt):
        """
        get all information about citizen
        """
        link = BASE_URL + ACTION['get'] + '?cmt={}'.format(cmt)
        return requests.get(link, headers= self.header).json()

    def count(self):
        """
        get number of rows in v-chain to make new CMT
        """
        link = BASE_URL + ACTION['search']
        nhommau = ['a', 'b', 'o', 'ab']
        json = [ {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "term": {
                                "nhommau": "{}".format(o)
                            }
                        }
                    ],
                    "must": [
                        {
                            "match": {
                                "nhommau": "{}".format(o)
                            }
                        }
                    ]
                }
            }
        } for o in nhommau]
        length = 0
        for j in json:
            length += len(requests.post(link, json= j, headers = self.header).json())
        return length + 3
    def post(self, hoten, anh, tenthuonggoi, ngaysinh, gioitinh, quequan, dantoc, tongiao, quoctich,noisinh,
             noithuongtru, noiohientai, nhommau, sohochieu, hotencha, hotenme, tinhtranghonnhan, hotenvochong, hotencon, ngaymat='', cmt= None):
        """
        if cmt = None: create new citizen
        else: update information of citizen
        """
        link = BASE_URL + ACTION['post']
        if cmt == None :
            cmt = self.count() + 1
        cmt = '{}'.format(cmt)
        json = {
          "quoctich": quoctich,
          "noiohientai": noiohientai,
          "gioitinh": gioitinh,
          "hotencha": hotencha,
          "sohochieu": sohochieu,
          "ngaysinh": ngaysinh,
          "hotenme": hotenme,
          "cmt": cmt,
          "noisinh": noisinh,
          "hotencon": hotencon,
          "ngaymat": ngaymat,
          "noithuongtru": noithuongtru,
          "dantoc": dantoc,
          "tongiao": tongiao,
          "quequan": quequan,
          "anh": anh,
          "hoten": hoten,
          "tenthuonggoi": tenthuonggoi,
          "tinhtranghonnhan": tinhtranghonnhan,
          "nhommau": nhommau,
          "hotenvochong": hotenvochong
        }
        requests.post(link, json=json, headers=self.header)
        return int(cmt)

# a = V_chainAPIs('a', '123', 'MANAGER')
# print(a.makeAuthentication())
def checkAuth(username, password):
    """
    make authentication token for user's account
    """
    link = BASE_URL + ACTION['authentication']
    json = {
        'username': username,
        'password': password
    }
    return requests.post(link, json=json).json()

# a = 1576596749
#
# import datetime
# # a = datetime.datetime.fromtimestamp(a).strftime('%d/%m/%Y')
# # print(a)
#
# c = b.get(2)
# temp = []
# length = len(c) - 1
# while length > 0:
#     c[length -1]['timestamp'] = datetime.datetime.fromtimestamp(c[length - 1]['timestamp']).strftime('%d/%m/%Y')
#     length -= 1
#     temp.append(c[length])
# print(temp[0])
# print(temp[1])