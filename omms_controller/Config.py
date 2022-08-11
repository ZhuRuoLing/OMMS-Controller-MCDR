from mcdreforged.api.all import *


class ServerMapping(Serializable):
    display_name: str = ""
    proxy_name: str = ""
    whitelist_name: str = ""

    def __str__(self):
        return f"{{{self.display_name},{self.proxy_name},{self.whitelist_name}}}"


class Config(Serializable):
    http_query_address: str = "localhost:50001"
    controller_name: str = "OMMS_Controller"
    friendly_name: str = "A Minecraft Server"
    uses_whitelist: str = "whitelist"
    unix_socket_file_path: str = ""
    channel: str = "GLOBAL"
    enable_mapping: bool = False
    server_mapping: list[ServerMapping] = []

    def __str__(self):
        mapping = "["
        for i in self.server_mapping:
            mapping += str(i)
        mapping += "]"
        return f"{self.controller_name},{self.friendly_name},{self.http_query_address},{self.uses_whitelist},{self.unix_socket_file_path},{self.channel},{mapping}"
