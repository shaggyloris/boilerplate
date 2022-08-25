from requests.auth import AuthBase


class TokenHeaderAuth(AuthBase):
    """
    Custom authentication mechanism that plugs into requests.
    
    APIClient class example:
    from apiclient import APIClient, TokenHeaderAuth

    class MyAPIClient(APIClient):
        def __init__(self, base_url, auth_token):
            super().__init__(base_url, auth=TokenHeaderAuth(auth_token))
            
        def get_my_data(self, params=None):
            resp = self.get('/my/data', params=params)
            return resp.json()
            
    def main():
        client = MyAPIClient('http://localhost:8000/api/v1/', "0ab260fb-0b29-405f-829a-3d519fdf2cc6")
        
        data = client.get_my_data()
        
        print(data)
        
        # Output: {'data': 'my data'}
    
    """
    def __init__(self, auth_token, header_key="Authorization", header_prefix="Bearer "):
        self.auth_token = auth_token
        self.header_key = header_key
        self.header_prefix = header_prefix

    def __call__(self, r):
        if not self.header_prefix:
            token = self.auth_token
        else:
            token = f"{self.header_prefix}{self.auth_token}"
        r.headers[self.header_key] = token
        return r
