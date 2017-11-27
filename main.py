#!/bin/python
import rpc
import time
from pycmus import remote

def parse(cmus_dict):
    status = {
        "state":cmus_dict["status"],
        "details":"No Song Selected",
        "assets": {
            "large_text": "c* music player",
            "large_image":"img_large"
        },
        "party": {
            "size":[1,1]
        }    
    }
    if cmus_dict["tag"] != {}:
        status["details"] = "{0} - {1}".format(cmus_dict["tag"]["artist"],cmus_dict["tag"]["title"])
    return status

client_id = "384747170403844117"
rpc = rpc.DiscordRPC(client_id)
rpc.start()
cmus = remote.PyCmus()

prev = cmus.get_status_dict()
rpc.send_rich_presence(parse(prev))

while True:
    status = cmus.get_status_dict()
    if status != prev:
        rpc.send_rich_presence(parse(status))
        prev = status
    time.sleep(15)
        