import pyeuropeana.apis as apis
import requests
from rich.console import Console
from rich.pretty import Pretty
from rich.table import Table
import apikey
import os
import json
from pathlib import Path

console = Console()

# import europeana key
europeana_api_key = apikey.load("EUROPEANA_API_KEY")
os.environ['EUROPEANA_API_KEY'] = europeana_api_key

# import trefle key
trefle_api_key = apikey.load("TREFLE_API_KEY")
os.environ['TREFLE_API_KEY'] = trefle_api_key

# function to take away instances of api keys in data
def redact_sensitive_data(value):
    if isinstance(value, dict):
        return {
            key: redact_sensitive_data(nested_value)
            for key, nested_value in value.items()
        }

    if isinstance(value, list):
        return [redact_sensitive_data(item) for item in value]

    if isinstance(value, str):
        redacted_value = value
        key_replacements = {
            europeana_api_key: "EUROPEANA_API_KEY",
            trefle_api_key: "TREFLE_API_KEY"
        }

        for api_key, replacement in key_replacements.items():
            if api_key:
                redacted_value = redacted_value.replace(api_key, replacement)
        return redacted_value

    return value

# function to display first value in field, used for the console table
def first_value(value, default="N/A"):
    if isinstance(value, list):
        return str(value[0]) if value else default
    return str(value) if value else default

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
    title = first_value(item.get("title"))
    item_type = first_value(item.get("type"))
    link = redact_sensitive_data(first_value(item.get("link")))

    # add values to the table, but this is really just for the visual
    table.add_row(title, item_type, link)

console.print(table)

final_data = {
    # "search_query": params["q"],
    "trefle_response": redact_sensitive_data(lavender_item),
    "europeana_response": redact_sensitive_data(europeana_items)
}

# had to use copilot to help structure exporting file to the current location
OUTPUT_FILE = Path(__file__).with_name("trefle_europeana_query_data.json")

with open(OUTPUT_FILE, "w") as f:
    json.dump(final_data, f, indent=4)

