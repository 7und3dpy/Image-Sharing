from getpass import getpass

from modules.utils import Utils
from modules.crypt import DiffieHellMan, PrimeGen

import requests, json

ip, port = None, None
logged_in = False
api_token, private_key = None, None
user_id, user_name = None, None

class Authentication: 
    def __init__(self, ip = '127.0.0.1', port = '5050'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'https://{0}:{1}'.format(self.__ip, self.__port)

    def register(self, name, public_key, key_length): 
        '''
        Register a new user. 

        Input: 
            - name: user name, 
            - public_key: user public_key (generated)
            - key_length: user key length (n)

        Output: 
            - user id

        Exception: 
            - thrown if any errors occured
        '''

        url = self.__default_url + '/register'

        res = requests.post(url, params= {
            'name': name, 
            'public_key': public_key, 
            'key_length': key_length
        })

        res = json.loads(res.text)

        if res['error']:
            raise Exception(res["message"])
        else: 
            return res["user_id"]
        
    def login(self, user_id, private_key): 
        '''
        Log user in
        '''
