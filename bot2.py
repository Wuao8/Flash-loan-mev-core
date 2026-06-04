import requests

print("TEST INTERNET BASE...")

try:
    r = requests.get("https://api.github.com", timeout=10)
    print("GitHub API status:", r.status_code)
except Exception as e:
    print("ERROR:", e)
