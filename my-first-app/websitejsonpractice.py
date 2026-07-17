import json
import urllib.request
from urllib.error import HTTPError, URLError


def ask_url():
    print("What website do you want to inspect?")
    url = input().strip()
    if not url:
        raise ValueError("No URL was entered.")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def fetch_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        body = response.read().decode("utf-8")
        return json.loads(body)


try:
    url = ask_url()
    data = fetch_json(url)
    print(json.dumps(data, indent=2))
except HTTPError as error:
    print(f"HTTP Error {error.code}: {error.reason}")
except URLError as error:
    print(f"URL Error: {error.reason}")
except ValueError as error:
    print(error)
except json.JSONDecodeError:
    print("The response was not valid JSON.")

