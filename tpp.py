#This script will show updates to the Twitch Plays Pokemon live feed on reddit.
#You can only show important updates by passing the --important flag when you run the script
#This could be easily adapted for other live feeds (or totally generic) but for now
#it is hardcoded for the TPP feed.

#python-requests is required to run this.
#Install using:
#pip install requests

from __future__ import print_function
import requests
import time
import argparse
import sys

_parser = argparse.ArgumentParser(description="Live Twitch Plays Pokemon updates in your console.")
_parser.add_argument("--important", action="store_true")
_args = _parser.parse_args()

_api_url = "http://api.reddit.com/live/t62j38i5dw54"
_headers = {"User-Agent": "TTPConsole/1.1 by sc00ty"}
_timeout = 60 #1 Minute
_last_id = ""

while True:
  try:
    #Request the JSON data for the live feed
    payload = {"before": _last_id}
    feed = requests.get(_api_url, params=payload, headers=_headers).json()

    #Iterate backwards through the list, making it so items are shown chronologically
    for feed_item in feed["data"]["children"][::-1]:
      #Store the last seen id
      _last_id = feed_item["data"]["name"]
      body_text = feed_item["data"]["body"]

      #If all text should be shown OR only important stuff, and this is important... show the update!
      if not _args.important or ("**" in body_text and _args.important):
        print("%s\n" % (body_text,))

    #Progress towards next update.
    for i in range (0, _timeout):
      print("Checking for update in %ss.\r" % (_timeout - i), end="")
      sys.stdout.flush()
      time.sleep(1)
  except KeyboardInterrupt:
    break
  except Exception:
    print("Encountered an error while retrieving data. Exiting...")
