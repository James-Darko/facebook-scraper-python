import facebook_scraper
import sys
import json
import requests.exceptions
import random

version = 7

def to_json(dict_var):
    return json.dumps(dict_var, default=str)

user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.99 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 12; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'
]

try:
    command = sys.argv[1]
    if command == "version":
        print(f"version {version}")
        exit(0)

    if len(sys.argv) < 5:
        print("ERROR: wrong number of arguments")
        exit(1)

    if len(sys.argv) == 6 and sys.argv[5] == "log":
        facebook_scraper.enable_logging()

    proxy = sys.argv[4]
    facebook_scraper.set_proxy(proxy)
    print(f"facebook-scraper-python v{version} - {sys.argv[2]} - {proxy}")
    if command == "feed":

        username = sys.argv[2]
        limit = int(sys.argv[3])
        cookies = {
            'c_user': "100090247007641",
            "xs": "14%3ALKkqzOtpkFwBPQ%3A2%3A1676654307%3A-1%3A-1"
        }
        # facebook_scraper.set_cookies(cookies)
        facebook_scraper.set_user_agent(random.choice(user_agents))
        posts = facebook_scraper.get_posts(account=username, options={"reactions": True})
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
    print("=================== proxy error ===================")
    if err.request.url == "https://facebook.com/settings":
        exit(3)
    if err.request.url == "http://lumtest.com/myip.json":
        exit(3)
    print(err.args[0])
    exit(2)
except requests.exceptions as err:
    print("=================== requests error ===================")
    print(err)
    print(err.args[0])
    print(err.request.url)
    exit(2)
except Exception as err:
    print("other error")
    print(err.args[0])
    exit(2)
