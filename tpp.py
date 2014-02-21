#This script will show updates to the Twitch Plays Pokemon live feed on reddit.
#You can only show important updates by passing the --important flag when you run the script
#This could be easily adapted for other live feeds (or totally generic) but for now
#it is hardcoded for the TPP feed.

#python-requests is required to run this.
#Install using:
#pip install requests

import requests
import time
import argparse
import sys

_parser = argparse.ArgumentParser(description="Live Twitch Plays Pokemon updates in your console.")
_parser.add_argument("--important", action="store_true")
_args = _parser.parse_args()

_api_url = "http://api.reddit.com/live/sw7bubeycai6hey4ciytwamw3a"
_headers = {"User-Agent": "TTPLiveConsole/1.0 by sc00ty"}
_timeout = 60 #1 Minute
_last_id = ""

while True:
  try:
    #Request the json data for the live feed
    payload = {"before": _last_id}
    feed_data = requests.get(_api_url, params=payload, headers=_headers).json()

    #Iterate backwards through the list, making it so items are shown chronologically
    for feed_item in feed_data["data"]["children"][::-1]:
      #Store the last seen id
      _last_id = feed_item["data"]["name"]
      body_text = feed_item["data"]["body"]

      #If all text should be shown OR only important stuff, and this is important... show the update!
      if not _args.important or ("**" in body_text and _args.important):
        print "%s\n" % (body_text,)

    #Progress towards next update.
    for i in range (0, _timeout):
      print "Checking for update in %ss.\r" % (_timeout - i),
      sys.stdout.flush()
      time.sleep(1)
  except KeyboardInterrupt:
    break