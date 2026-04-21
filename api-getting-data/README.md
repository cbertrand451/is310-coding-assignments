# GETting Culture Across APIs

For this assignment, I chose to work with the [Trefle API](https://trefle.io/). This API is a datasource for botanical and global plants. I have a hobby for houseplants, and wanted to use an API that I would be interested in, but still have relevant data to the Europeana database. 

I had to brainstorm a plant that would likely have multiple uses or historical data. I leaned away from modern houseplants like a Monstera or Pothos, just because I wasn;t sure how much data would show up on Europeana. I chose ***Lavender*** as a botanincal to explore, because I know it has meidacal and herbal pruposes that may appear in historical data. 

### How I Used Trefle API

The API documentation was pretty straight forward. The documentation gave examples for how to search for specific series:

```
import requests

r = requests.get('https://trefle.io/api/v1/species/search?q=coconut&token=YOUR_TREFLE_TOKEN')
r.json
```
I replaced that query with *"lavender"* instead, and filtered the item name to be eactly "lavender", since there were a lot of  results with more specific species. 

### How I used Europeana API

I took the information I got straight from the Trefle API reponse and used it in the query for Europeana. I took the scientific name for Lavender, which in this case was ***"Lavandula angustifolia"***, and used that as the search query. 

I structured the top ten responses into **title**, **item type**, and **link** to display the info cleanly in the CLI, and then used the top ten results from Europeana API, unedited besides for instances of the api key, in the final json. 
