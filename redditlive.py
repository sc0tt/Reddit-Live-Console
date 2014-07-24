from __future__ import print_function
import requests
import time
import sys
import re

_headers = {"User-Agent": "TTPConsole/1.1 by sc00ty"}
_timeout = 60  # 1 Minute


def main(live_thread):
  _last_id = ""
  while True:
    try:
      #Request the JSON data for the live feed
      payload = {"before": _last_id}
      feed = requests.get(live_thread, params=payload, headers=_headers).json()

      #Iterate backwards through the list, making it so items are shown chronologically
      for feed_item in feed["data"]["children"][::-1]:
        #Store the last seen id
        _last_id = feed_item["data"]["name"]
        body_text = feed_item["data"]["body"]

        print("%s\n" % (body_text,))

      #Progress towards next update.
      for i in range(0, _timeout):
        print("Checking for update in %ss.\r" % (_timeout - i), end="")
        sys.stdout.flush()
        time.sleep(1)
    except KeyboardInterrupt:
      break
    #except Exception:
    #  print("Encountered an error while retrieving data. Exiting...")
    #  break


def get_live_thread_url(thread_id):
  id_re = re.search("(/live/)?([A-z0-9]+)$", thread_id).groups()

  if not id_re or not id_re[1]:
    raise Exception("Invalid live thread.")

  return "http://reddit.com/live/%s.json" % id_re[1]

if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise Exception("Please include a thread URL or ID.")

  thread = get_live_thread_url(sys.argv[1])
  main(thread)