#!/bin/python
import rpc
import time
from pycmus import remote

defaultstatus = {
        "state":"stopped",
        "details":"Not playing",
        "assets": {
            "large_text": "c* music player",
            "large_image":"main_logo"
        }
    }

def parse(cmus_dict):
    status = {
        "state":cmus_dict["status"],
        "details":"Not playing",
        "assets": {
            "large_text": "c* music player",
            "large_image":"main_logo"
        }
    }
    if cmus_dict["tag"] != {}:
        status["state"] = "{0}".format(cmus_dict["tag"]["title"])
        status.pop("details")
        status["assets"]["large_text"] = "{0}".format(cmus_dict["tag"]["album"])
        status["assets"]["small_image"] = "artist_logo"
        status["assets"]["small_text"] = "{0}".format(cmus_dict["tag"]["artist"])
        status["timestamps"] = { 
            "start": int(time.time()) - int(cmus_dict["position"]),
            "end": int(time.time()) - int(cmus_dict["position"]) + int(cmus_dict["duration"])
        }
    return status

client_id = "409516139404853248"
rpc = rpc.DiscordRPC(client_id)
rpc.start()
print("RPC init finished")
cmus = remote.PyCmus()
print("cmus connection opened")

prev = cmus.get_status_dict()
rpc.send_rich_presence(parse(prev))

while True:
    status = cmus.get_status_dict()
    if status != prev:
        rpc.send_rich_presence(parse(status))
        prev = status
    if status == prev:
        if status["status"] == "paused" or status["status"] == "stopped":
            rpc.send_rich_presence(defaultstatus)
    time.sleep(15)
        