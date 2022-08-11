from .Config import *
from .Util import *
from .UdpBroadcast import *
import socket

from .httpclient.HttpConnector import *
from .httpclient.HttpRequestTypes import *

config: Config
default_config = Config()
connector: HttpConnector


def on_load(server: PluginServerInterface, old_module):
    global connector
    global config
    config = server.load_config_simple(target_class=Config, default_config=get_default_config())
    server.logger.info(config)
    connector = HttpConnector(config.http_query_address)
    udp_broadcast_receiver(server, config)
    server.logger.info("Done!")


""""It works!"""


def on_player_left(server: PluginServerInterface, player_name: str):
    message = {
        "channel": config.channel,
        "server": config.friendly_name,
        "player": player_name,
        "content": "我不打扰，我走了哈"
    }
    json_text = json.dumps(message)
    data = json_text.encode("utf-8")
    s = socket.socket(type=socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 10086))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 64)
    s.setsockopt(socket.IPPROTO_IP,
                 socket.IP_ADD_MEMBERSHIP,
                 socket.inet_aton("224.114.51.4") + socket.inet_aton("0.0.0.0"))
    s.setblocking(True)
    s.sendto(data, ("224.114.51.4", 10086))
    s.close()
    pass


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    global connector
    message = {
        "channel": config.channel,
        "server": config.friendly_name,
        "player": player,
        "content": "我TM勑"
    }
    json_text = json.dumps(message)
    data = json_text.encode("utf-8")
    s = socket.socket(type=socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 10086))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 64)
    s.setsockopt(socket.IPPROTO_IP,
                 socket.IP_ADD_MEMBERSHIP,
                 socket.inet_aton("224.114.51.4") + socket.inet_aton("0.0.0.0"))
    s.setblocking(True)
    s.sendto(data, ("224.114.51.4", 10086))
    s.close()
    server.logger.debug(f"Player {player} joined.")
    result = connector.request(type=HttpRequestTypes.QUERY_PLAYER_IN_ALL_WHITELIST, player=player)
    if result is not None:
        if not config.enable_mapping:
            return
        result: list
        mapping = config.server_mapping
        title = f"--------------- {config.friendly_name} ----------------"
        greet = "欢迎！点击下面的名字以进入对应服务器。"
        parts1 = []
        whitelists_in_mapping = []
        # mapping -> result
        for m in mapping:
            m: ServerMapping
            # WTF
            whitelists_in_mapping.append(m.whitelist_name)
            if m.whitelist_name in result:
                if m.display_name == config.friendly_name:
                    server_text = RText(m.display_name) \
                        .set_color(RColor.gold).set_hover_text(f"您现在在此服务器")
                    parts1.append(RTextList("[", server_text, "]"))
                else:
                    server_text = RText(m.display_name) \
                        .set_click_event(RAction.run_command, f"/server {m.proxy_name}") \
                        .set_color(RColor.green) \
                        .set_hover_text(f"去{m.display_name}")
                    parts1.append(RTextList("[", server_text, "]"))
            else:
                pass
        # result -> mapping
        not_included_servers = []
        for r in result:
            r: str
            if (r not in whitelists_in_mapping) and ():
                server_text = RText(r) \
                    .set_color(RColor.green) \
                    .set_hover_text(
                    RText("Mapping might not properly configured,please use /server.").set_color(RColor.red))
                not_included_servers.append(RTextList("[", server_text, "]"))
        # THAT MAKES ME BIG BRAIN
        parts1.extend(not_included_servers)
        servers = RTextList(*parts1)
        server.tell(player=player, text=title)
        server.tell(player=player, text=greet)
        server.tell(player=player, text=RText(""))
        server.tell(player=player, text=servers)

    else:
        if server.is_server_running():
            server.execute(f"kick {player} 你不在白名单中")


"""
mapping: 1 2 3 4 5
result: 3 4 5 6
6 not in mapping
"""


@new_thread("Sender")
def on_user_info(server: PluginServerInterface, info: Info):
    """
    send_time = json_dict.get("time")
            from_server = json_dict.get("server")
            from_player = json_dict.get("player")
            content = json_dict.get("content")
    """
    if not info.is_player:
        return
    message = {
        "channel": config.channel,
        "server": config.friendly_name,
        "player": info.player,
        "content": info.content
    }
    json_text = json.dumps(message)
    data = json_text.encode("utf-8")
    s = socket.socket(type=socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 10086))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 64)
    s.setsockopt(socket.IPPROTO_IP,
                 socket.IP_ADD_MEMBERSHIP,
                 socket.inet_aton("224.114.51.4") + socket.inet_aton("0.0.0.0"))
    s.setblocking(True)
    s.sendto(data, ("224.114.51.4", 10086))
    s.close()
