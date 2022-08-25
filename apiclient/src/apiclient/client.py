import requests


class APIClient:
    """
    An abstract class that utilizes the requests library to create an api client
    
    example usage:
    
    from apiclient import APIClient
    from requests.auth import HTTPBasicAuth
    
    class MyAPIClient(APIClient):
        def get_my_data(self, params=None):
            resp = self.get('/my/data', params=params)
            return resp.json()
            
    def main():
        client = MyAPIClient('http://localhost:8000/api/v1/', HTTPBasicAuth('user', 'pass'))
        
        data = client.get_my_data()
        
        print(data)
        
        # Output: {'data': 'my data'}
    
    """
    
    def __init__(self, base_url, auth=None, headers=None, timeout=(30, 90), verify=True):
        self.base_url = base_url
        self.auth = auth
        self.verify = verify
        self.headers = headers
        self.timeout = timeout
        self.session = self._init_session()
        
    def _init_session(self):
        """
        Initializes a session for the api client
        """
        session = requests.Session()
        session.auth = self.auth
        session.verify = self.verify
        if self.headers:
            session.headers.update(self.headers)
        return session
    
    def get(self, path, params=None):
        """
        Performs a GET request to the api
        """
        return self.request('GET', path, params=params)
    
    def post(self, path, data=None):
        """
        Performs a POST request to the api
        """
        return self.request('POST', path, data=data)
    
    def put(self, path, data=None):
        """
        Performs a PUT request to the api
        """
        return self.request('PUT', path, data=data)
    
    def delete(self, path, data=None):
        """
        Performs a DELETE request to the api
        """
        return self.request('DELETE', path, data=data)
    
    def request(self, method, path, **kwargs):
        """
        Performs a request to the api
        """
        url = self.base_url + path
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        # We raise for status here to allow the custom client to handle the error
        response.raise_for_status()
        return response
