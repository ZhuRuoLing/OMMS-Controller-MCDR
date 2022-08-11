import json
import socket
import threading

from .Config import *


@new_thread("UdpBroadcastReceiver")
def udp_broadcast_receiver(server: PluginServerInterface, config: Config):
    threads = threading.enumerate()
    names = []
    for t in threads:
        names.append(t.name)
    if names.count("UdpBroadcastReceiver") >= 2:
        return
    server.logger.info("Started Broadcast receiver thread.")
    s = socket.socket(type=socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 10086))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 64)
    s.setsockopt(socket.IPPROTO_IP,
                 socket.IP_ADD_MEMBERSHIP,
                 socket.inet_aton("224.114.51.4") + socket.inet_aton("0.0.0.0"))
    s.setblocking(True)
    while True:
        try:
            data, address = s.recvfrom(114514)
            json_str = data.decode("utf-8")
            json_dict: dict = json.loads(json_str)
            from_server = json_dict.get("server")
            from_player = json_dict.get("player")
            channel = json_dict.get("channel")
            content = json_dict.get("content")
            if config.friendly_name == from_server:
                continue
            server_ = RText(from_server).set_color(RColor.yellow).set_styles(RStyle.bold)
            player = RText(from_player).set_color(RColor.green)

            final_rtext = RTextList(channel, " <", player,
                                    RText("[").set_color(RColor.green),
                                    server_,
                                    RText("]> ").set_color(RColor.green)
                                    , content)
            if server.is_server_running():
                server.broadcast(final_rtext)
        except Exception as e:
            server.logger.info(str(e))
    # 224.114.51.4:10086
