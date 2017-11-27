# PyDiscordRPC
Originally created by [GiovanniMCMXCIX](https://github.com/GiovanniMCMXCIX/PyDiscordRPC), this script has been modified so that you can easily import it into your own Python projects (It could definately be improved for sure). For more information on Discord's Rich Presence feature, look here: https://discordapp.com/developers/docs/rich-presence/best-practices

# How To Use
Here's a quick example script on how to use this module:

```Python
import rpc
import time

client_id = '1234567892138470' #Your application's client ID as a string. (This isn't a real client ID)
RPC = rpcpy.DiscordRPC(client_id) #Send the client ID to the rpc module
RPC.start() #Start the RPC connection

current_time = time.time()

#This is the activity information sent to the client
activity = {
    "state": "This is the state",
    "details": "Here are some details",
    "timestamps": {
        "start": int(current_time)
    },
    "assets": {
        "small_text": "Text for small_image",
        "small_image": "img_small",
        "large_text": "Text for large_image",
        "large_image": "img_large"
    },
    "party": {
        "size": [1, 6]
    }
}

RPC.send_rich_presence(activity)
time.sleep(60)
 #Presence is set for 60 seconds, afterwards the script will end and the presence will disappear from your profile.
 ```

You can see a more practical use where I use this to report to Discord the song I have playing in Winamp [here](https://github.com/DerpyChap/Winamp-Discord-RPC).
