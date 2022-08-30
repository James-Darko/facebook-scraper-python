import facebook_scraper
from facebook_scraper import _scraper
import sys
import json
import requests.exceptions
import random

def to_json(dict_var):
    return json.dumps(dict_var, default=str)

if len(sys.argv) != 5:
    print("ERROR: wrong number of arguments")
    exit(1)

user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.99 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 12; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'
]

try:
    proxy = sys.argv[4]
    # facebook_scraper.set_proxy("http://209.205.212.34:1207")
    facebook_scraper.set_proxy(proxy)
    print("facebook-scraper-python v4 - " + proxy)
    command = sys.argv[1]
    if command == "feed":
        # username = "bobshideout"
        username = sys.argv[2]
        limit = int(sys.argv[3])
        cookies = {
            'c_user': "100085031296303",
            "xs": "18%3Azc1VkQWpSd-VfA%3A2%3A1661877613%3A-1%3A-1%3A%3AAcUsQNlzCx9LtzFJKEb4hZJ7sg0f8QLTuuFI4ChMWg"
        }
        facebook_scraper.set_cookies(cookies)
        facebook_scraper.set_user_agent(random.choice(user_agents))
        posts = facebook_scraper.get_posts(account=username, options={"reactions": True})
        # for post in posts:
        #     print(post)
        with open(username + ".txt", "w") as f:
            count = 0
            for post in posts:
                s = to_json(post)
                print(s)
                f.write(s + "\n")
                count += 1
                if count >= limit:
                    break

    elif command == "post":
        url = sys.argv[2]
        file = sys.argv[3]
        posts = facebook_scraper.get_posts(post_urls=[url], options={"reactions": True})
        with open(file, "w") as f:
            post = next(posts)
            f.write(to_json(post))
    else:
        print("unknown command: " + command)
        exit(1)
except requests.exceptions.ProxyError as err:
    print(err)
    exit(2)