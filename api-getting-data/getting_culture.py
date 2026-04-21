import pyeuropeana.apis as apis
import requests
from rich.console import Console
from rich.pretty import Pretty
from rich.table import Table
import apikey
import os
import json

console = Console()

# import europeana key
europeana_api_key = apikey.load("EUROPEANA_API_KEY")
os.environ['EUROPEANA_API_KEY'] = europeana_api_key

# import trefle key
trefle_api_key = apikey.load("TREFLE_API_KEY")
os.environ['TREFLE_API_KEY'] = trefle_api_key

# define trefle endpoint and parameters for call
# chose lavender, because it will likely have data from europeana as well
url = "https://trefle.io/api/v1/species/search"
params = {
    "q": "lavender",
    "token": trefle_api_key
}

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

# filtered for an exact item match, which is just "lavender" in this case
for item in data['data']:
    if item.get("common_name").lower() == params["q"]:
        lavender_item = item
        break

console.print(f"\n[purple]First three Trefle responses for [bold white]{params['q']}[/bold white]:[/purple]\n")
console.print(Pretty(data["data"][:3]))

# using the scientific name to search europeana instead of basic name 
euro_query =  lavender_item.get("scientific_name")

response = apis.search(query=euro_query, rows=10)
europeana_items = response.get("items", [])

console.print(f"\n[purple]Top ten Europeana search results for [bold white]{euro_query}[/bold white]:[/purple]\n")


table = Table(show_lines=True)

table.add_column("Title", style="purple", overflow="fold")
table.add_column("Type", style="yellow")
table.add_column("Link", style="blue")

for item in response.get("items", []):
    title = item.get("title", "N/A")
    item_type = item.get("type", "N/A")
    link = item.get("link", "N/A")

    # europeana results were coming back as lists, so I just took the first item
    # did it for every value just in case
    if isinstance(title, list):
        if title:
            title = title[0] 
        else:
            title = "N/A"
    else:
        title = str(title)

    if isinstance(item_type, list):
        if item_type:
            item_type = item_type[0] 
        else:
            item_type = "N/A"
    else:
        item_type = str(item_type)

    if isinstance(link, list):
        if link:
            link = link[0] 
        else:
            link = "N/A"
    else:
        link = str(link)

    # add values to the table, but this is really just for the visual and the original values will be in the json
    table.add_row(title, item_type, link)

console.print(table)

final_data = {
    # "search_query": params["q"],
    "trefle_response": lavender_item,
    "europeana_response": europeana_items
}

with open("trefle_europeana_query_data.json", "w") as f:
    json.dump(final_data, f, indent=4)


