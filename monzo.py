"""Methods to access MONZO API Endpoints"""

import os
import json

from .auth import MonzoAuthClient

class Monzo():
    __api_url = "https://api.monzo.com"

    auth_client:'MonzoAuthClient'
    
    __token_filename = "monzo.json"
    def __init__(self, auth_client:'MonzoAuthClient') -> None:
        self.auth_client = auth_client

    def whoami(self):
        api_rel_path = "/ping/whoami"
        request_url = f"{self.__api_url}{api_rel_path}"
        response = self.auth_client.make_request(url=request_url)

        return response

    def get_accounts(self):
        api_rel_path = "/accounts"
        request_url = f"{self.__api_url}{api_rel_path}"
        acc_list = self.auth_client.make_request(url=request_url)["accounts"]
        return acc_list

    def get_balance(self, acc_n = 0):
        api_rel_path = "/balance"
        request_url = f"{self.__api_url}{api_rel_path}"

        acc_list = self.get_accounts()
        acc = acc_list[acc_n]

        params = {}
        params['account_id'] = acc['id']

        balance = self.auth_client.make_request(url=request_url, params=params)
        return balance

    def get_pots(self, acc_n:int=0, return_deleted:bool=False):
        api_rel_path = "/pots"
        request_url = f"{self.__api_url}{api_rel_path}"

        acc_list = self.get_accounts()
        acc = acc_list[acc_n]

        params = {}
        params['current_account_id'] = acc['id']
        pot_list = self.auth_client.make_request(url=request_url, params=params)["pots"]
        print(len(pot_list))

        if return_deleted == True: return pot_list

        pot_list_filter = []
        for pot in pot_list:
            if pot['deleted'] == False: 
                pot_list_filter.append(pot)

        return pot_list_filter

    def get_pot(self, pot_num:int=0, pot_name:str=None, pot_id:str=None):
        """
        Get Specific Pot.
        Define none or ONLY one (1) input:
        :param: pot_num     - returns nth pot in returned list of pots
        :param: pot_name    - return pot by name
        :param: pot_id      - return pot by id

        :rtype: dict
        """

        pot_list = self.get_pots()

        if pot_id:
            pot = next((item for item in pot_list if item['id'] == pot_id), None)
            return pot
        
        if pot_name:
            pot = next((item for item in pot_list if item['name'] == pot_name), None)
            return pot
        
        pot = pot_list[pot_num]
        return pot
        