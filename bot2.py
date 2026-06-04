import requests

print("Test connessione Jupiter...")

url = "https://price.jup.ag/v4/price?ids=SOL"

response = requests.get(url)

print("Status Code:", response.status_code)
print("Risposta API:")
print(response.text)
