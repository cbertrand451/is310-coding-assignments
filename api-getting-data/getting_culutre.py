import pyeuropeana.apis as apis
import pyeuropeana.utils as utils
import requests
from rich.console import Console
from rich.pretty import Pretty
import apikey
import os

console = Console()

# import europeana key
europeana_api_key = apikey.load("EUROPEANA_API_KEY")
os.environ['EUROPEANA_API_KEY'] = europeana_api_key

# import trefle key
trefle_api_key = apikey.load("TREFLE_API_KEY")
os.environ['TREFLE_API_KEY'] = trefle_api_key

url = "https://trefle.io/api/v1/species/search"
params = {
    "q": "lavender",
    "token": trefle_api_key
}

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

for item in data['data']:
    if item.get("common_name").lower() == params["q"]:
        lavender_item = item
        break

console.print(f"\n[green]Trefle response for [bold white]{params['q']}[/bold white]:[/green]\n")
console.print(Pretty(lavender_item))



