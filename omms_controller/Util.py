from .Config import *


def generate_random_str(str_len=8):
    import random
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(str_len):
        random_str += base_str[random.randint(0, length)]
    return random_str


def get_default_config():
    config = Config()
    config.controller_name = f"OMMS_Controller_{generate_random_str(8)}"
    config.uses_whitelist = "whitelist"
    config.unix_socket_file_path = None
    config.channel = "GLOBAL"
    config.server_mapping = list[ServerMapping]()
