from enum import Enum


class HttpRequestTypes(Enum):
    GET_WHITELIST_NAMES = 0
    GET_WHITELIST_CONTENTS = 1
    QUERY_PLAYER = 3
    QUERY_PLAYER_IN_ALL_WHITELIST = 4