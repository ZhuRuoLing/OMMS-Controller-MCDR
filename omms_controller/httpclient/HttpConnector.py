from typing import Tuple
from .HttpRequestTypes import HttpRequestTypes
from mcdreforged.api.all import *
import requests


class HttpConnector:
    addr: str = ""

    def __init__(self, addr: str):
        self.addr = addr

    def request(self, **kwargs):
        type: HttpRequestTypes = kwargs["type"]
        url: str = f"http://{self.addr}/whitelist/"
        match type:
            case HttpRequestTypes.QUERY_PLAYER:
                url = url + kwargs["whitelist"] + "/query/" + kwargs["player"]
                request = requests.get(url=url)
                if request.status_code == 200:
                    return True
                return False
                pass
            case HttpRequestTypes.GET_WHITELIST_NAMES:
                request = requests.get(url=f"http://{self.addr}/whitelist")
                if request.status_code == 200:
                    if request.text == "No Whitelists found.":
                        return None
                    return request.json()
                return None
                pass
            case HttpRequestTypes.GET_WHITELIST_CONTENTS:
                url = url + kwargs["whitelist"]
                request = requests.get(url=url)
                if request.status_code == 200:
                    return request.json()
                return None
                pass
            case HttpRequestTypes.QUERY_PLAYER_IN_ALL_WHITELIST:
                url = url + "queryAll/" + kwargs["player"]
                request = requests.get(url=url)
                if request.status_code == 200:
                    whitelists: list = request.json()
                    return whitelists
                return None
                pass
            case _:
                return
