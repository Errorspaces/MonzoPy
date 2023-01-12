import json

from requests_oauthlib import OAuth2Session

from functions.util_functions import save_token_to_file
from monzo.error import (
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    MethodNotAllowedError,
    PageNotFoundError,
    NotAcceptableError,
    TooManyRequestsError,
    InternalServerError,
    GatewayTimeoutError
)

class MonzoAuthClient():
    __auth_url = "https://auth.monzo.com"
    __api_url = "https://api.monzo.com"
    
    __token_filename = "monzo_token.json"

    client_id:str
    client_secret:str


    def __init__(
        self, 
        client_id:str, 
        client_secret:str,
        state:str=None,
        access_token:str=None,
        refresh_token:str=None,
        expires_at:float=None
        ) -> None:

        self.client_id = client_id
        self.client_secret = client_secret

        token = {}
        if access_token:
            token['access_token'] = access_token
        if refresh_token:
            token['refresh_token'] = refresh_token
        if expires_at:
            token['expires_at'] = expires_at

        self.session = OAuth2Session(
            client_id=self.client_id,
            token_updater=save_token_to_file,
            state=state
        )


    def first_auth(self, redirect_uri=None):
        authorization_url = self.create_authorization_url(redirect_uri=redirect_uri)
        print(f"Follow Link and Authorize with Email: \n {authorization_url}")

        code = input(f"Enter Code: ")

        token = self.generate_token(code=code)

    def auth_from_file(self, filename=__token_filename):
        with open(file=filename) as f:
            token = json.load(f)
        
        self.session.token = token

    def make_request(self, url:str, method="GET", **kwargs):

        response = self.session.request( url=url, method=method,**kwargs)
        response = self.validate_response(response)
        return response

    def create_authorization_url(self, redirect_uri=None):
        if redirect_uri:
            self.session.redirect_uri = redirect_uri

        return self.session.authorization_url(self.__auth_url)[0]

    def generate_token(self, code:str):
        token_request_url = f"{self.__api_url}/oauth2/token"
        
        token = self.session.fetch_token(
            token_url=token_request_url,
            username=self.client_id,
            password=self.client_secret,
            code=code,
            # include_client_id=True
        )
        token['client_secret'] = self.client_secret

        if self.session.token_updater:
            self.session.token_updater(token, filename=self.__token_filename)

        return token
    
    def validate_response(self, response):
        json_response = response.json()
        if response.status_code == 200:
            return json_response
        if response.status_code == 400:
            raise BadRequestError(json_response["message"])
        if response.status_code == 401:
            raise UnauthorizedError(json_response["message"])
        if response.status_code == 403:
            raise ForbiddenError(json_response["message"])
        if response.status_code == 404:
            raise PageNotFoundError(json_response["message"])
        if response.status_code == 405:
            raise MethodNotAllowedError(json_response["message"])
        if response.status_code == 406:
            raise NotAcceptableError(json_response["message"])
        if response.status_code == 429:
            raise TooManyRequestsError(json_response["message"])
        if response.status_code == 500:
            raise InternalServerError(json_response["message"])
        if response.status_code == 504:
            raise GatewayTimeoutError(json_response["message"])