#!/bin/python
import rpc
import time
import re
import signal
import sys
import yaml
import os
from pycmus import remote
from shutil import copyfile


def config_loader():
    if not os.path.isfile('config.yaml'):
        copyfile('config.yaml.example', 'config.yaml')
    with open('config.yaml', 'r') as configfile:
        config = yaml.safe_load(configfile)
    print('Config file loaded.')
    return config


def signal_handler(signal, frame):
    rpc.close()
    sys.exit(0)


def parse(cmus_dict):
    status = {
        "state": cmus_dict["status"],
        "details": "Not playing",
        "assets": {
            "large_image": "main_logo"
        }
    }
    if cmus_dict["tag"]:
        status["state"] = "{0}".format(cmus_dict["tag"]["title"])
        status.pop("details")
        if cmus_dict["tag"]["album"]:
            status["assets"]["large_text"] = "{0}".format(cmus_dict["tag"]["album"])
        if cmus_dict["tag"]["artist"]:
            status["assets"]["small_image"] = "artist_logo"
            status["assets"]["small_text"] = "{0}".format(cmus_dict["tag"]["artist"])
        if config["start_time"]:
            status["timestamps"] = {
                "start": int(time.time()) - int(cmus_dict["position"])
            }
        else:
            status["timestamps"] = {
                "end": int(time.time()) - int(cmus_dict["position"]) + int(cmus_dict["duration"])
            }

    elif cmus_dict["status"] == "playing" or cmus_dict["status"] == "paused":
        filename = re.match(".*\/([^\.]+)\..", cmus_dict["file"]).group(1)  # regex by @LiquidFenrir :)
        status["details"] = "{0}".format(filename)
    return status


client_id = "409516139404853248"
rpc = rpc.DiscordRPC(client_id)
rpc.start()
print("RPC init finished")
cmus = remote.PyCmus()
print("cmus connection opened")

signal.signal(signal.SIGINT, signal_handler)

config = config_loader()

while True:
    status = cmus.get_status_dict()
    rpc.send_rich_presence(parse(status))
    time.sleep(15)
