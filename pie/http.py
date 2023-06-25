import requests
from typing import Callable

METHOD = {0: "get", 1: "post"}

class Client:
    def __init__(self, bearer_token: str, *, client_number_id = None):
        self.client_number_id = client_number_id 
        self.bearer_token: str = bearer_token
        self.base_url: str = "https://graph.facebook.com/v17.0"
        self.raw_data: dict = {
            "unfinish_message_data": lambda to, type: 
            {
                "messaging_product": "whatsapp", "to": str(to), "type": str(type)
            }
        }
        self.endpoints: dict = {
            "/messages": f"https://graph.facebook.com/v17.0/{client_number_id}/messages"
        }
        self.request = requests.request

    def _request(self, root: Callable, method:int, data: dict, headers = {}, **kwargs):
        try:
            method = METHOD[method]
            url = self.endpoints[root]
        except KeyError:
            raise KeyError("Method or url not found!")

        if not "Authorization" in headers.keys():
            headers["Authorization"] = "Bearer " + self.bearer_token
            
        if kwargs.get("FROM_ID") is not None:
            root = root(kwargs["FROM_ID"])

        return self.request(method, url, json=data, headers = headers)

    def send_message(self, to: int, *, type: str, body: str):
        if not self.client_number_id:
            raise ValueError("This function requires you to put the client's number id as an extra keyword argument in your client!")
            
        data = self.raw_data["unfinish_message_data"](to, type)

        if body:
            data["text"] = {"body": body}
        
        return self._request("/messages", 1, data)