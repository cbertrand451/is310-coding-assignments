# Fandom Wikis and Web Scraping

This folder contains my script for scraping the Marvel Fandom Wiki with Python. The script scrapes Marvel movie data. 

I chose to scrape the Marvel Movies from this fandom, because it held a considerable amount of data, and the data was consistent across the pages. A lot of the other Wikis I visited seemed patchy and inconsistent. This data may be useful to researchers studying film productions, or the timeline of a franchise, and it's growth across the movies it releases. 

***robots.txt***: https://marvel.fandom.com/robots.txt

Here is the link to the *robots.txt*, which allows for web scraping for **User-agent**. The only 
pages that weren;t allowed to be scraped were **user** pages and **special** pages, which the movies fell under neither. 


### WARNING

The script may take a second to finish because it first scrapes the main Marvel
Films page, then opens and scrapes each individual movie page before writing the
CSV file. There should be 47 movies scraped in total, so it might not be instant. 

## Using *fandom_wiki_scraping.py*

### Install the required libraries

Before running the script, install the Python libraries it uses:

*pip install cloudscraper beautifulsoup4*


The script depends on:

- *cloudscraper* to request pages from Fandom
- *beautifulsoup4* to parse the HTML and pull out movie links and infobox data
- *csv* to write the scraped data into a CSV file

### Run the script

From the root of this repository, run:

*python web-scraping/fandom_wiki_scraping.py*

### What the script does

The first step is requesting the Marvel Films page on the Marvel Fandom wiki:

https://marvel.fandom.com/wiki/Marvel_Films

Then it uses BeautifulSoup to find the movie sections for the 2000s, 2010s, and
2020s. There were way too many mvoies on the actual page, and the ones under these sections seemed
the most mainstream. 

The script collects each valid Marvel movie wiki link while skipping
duplicate links and non-movie links. There were lots of links like files, categories, or special pages
that kept getting picked up by the scraper, and had to be filtered out. Choosing to only download from certain decades helped this problem a lot. 

After it collects the movie links, it visits each individual movie page and
looks for the page's portable infobox, which is like a table with all of the details I was loooking for. 

Once all movie pages have been scraped, the script writes the results to *marvel_movies.csv*


