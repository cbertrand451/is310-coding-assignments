import cloudscraper
from bs4 import BeautifulSoup
import csv

base_url = "https://marvel.fandom.com"
films_url = base_url + "/wiki/Marvel_Films"

# define the scraper and reponse 
scraper = cloudscraper.create_scraper()


def get_page_soup(url):
    response = scraper.get(url)

    if response.status_code != 200:
        print("Script not working!")
        return None

    return BeautifulSoup(response.text, "html.parser")

# some of the headers had extra whitespace
def normalize_heading(text):
    text = clean_text(text).lower()
    return "".join(character for character in text if character.isalnum())

# add the link to the list if its seen as an ok movie
def add_movie_link(link, movie_links, seen_urls):
    href = link.get("href")
    title = link.get("title")

    # Keep only regular wiki article links
    # File: Category: Special: and other ones were found as links that I didnt want
    if not href or not title or not href.startswith("/wiki/") or ":" in href:
        return

    full_url = base_url + href
    if full_url in seen_urls:
        return

    seen_urls.add(full_url)
    movie_links.append({
        "title": clean_text(title),
        "url": full_url
    })


def get_movie_links(soup):
    movie_links = []
    # had to remove duplicate because some movies were listed multipls times, so used a set
    seen_urls = set()

    # used this to grab the specific section of the page underneth the different decades
    content = soup.select_one(".mw-parser-output")
    if not content:
        return movie_links

    decade_sections = {"2000s", "2010s", "2020s"}
    collecting = False

    # decade sections were h3 tags 
    # had to use copilot to help structure this, as i was having trouble grabbing the correct section
    for element in content.find_all(recursive=False):
        if element.name in ["h2", "h3"]:
            headline = element.find(class_="mw-headline")
            section_title = normalize_heading(headline.get_text() if headline else element.get_text())
            collecting = element.name == "h3" and section_title in decade_sections
            continue

        if collecting:
            for link in element.find_all("a", href=True, title=True):
                add_movie_link(link, movie_links, seen_urls)

    return movie_links


def get_movies():
    soup = get_page_soup(films_url)
    if not soup:
        return []

    movies = get_movie_links(soup)

    # print(f"Found {len(movies)} movie links")
    return movies


# remove extra whitespace and newlines from text
def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split()).strip()

# main function for scraping each movie individually
# found that the html is an infobox and data is in "pi-data"
def scrape_movie_page(url):
    response = scraper.get(url)

    if response.status_code != 200:
        print(f"Failed to load: {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # data that the script will be looking for, and will fill them with empty values if not foun
    movie_data = {
        "title": "",
        "page_url": url,
        "aliases": "",
        "release_dates": "",
        "directors": "",
        "producers": "",
        "comic_book_writers": "",
        "screenplay_writers": "",
        "musicians": "",
        "cinematographers": "",
        "editors": "",
        "distributors": "",
        "production_companies": "",
        "running_time": "",
        "rating": "",
        "budget": "",
    }

    infobox = soup.find("aside", class_="portable-infobox")
    if not infobox:
        print(f"No infobox found for: {url}")
        return movie_data

    # Page title from infobox title if it's available
    title_tag = infobox.find("h2", class_="pi-title")
    if title_tag:
        movie_data["title"] = clean_text(title_tag.get_text())
    else:
        h1 = soup.find("h1")
        if h1:
            movie_data["title"] = clean_text(h1.get_text())

    field_map = {
        "title": "title",
        "aliases": "aliases",
        "release date(s)": "release_dates",
        "directors": "directors",
        "producers": "producers",
        "comic book writers": "comic_book_writers",
        "screenplay writers": "screenplay_writers",
        "musicians": "musicians",
        "cinematographers": "cinematographers",
        "editors": "editors",
        "distributors": "distributors",
        "production companies": "production_companies",
        "running time": "running_time",
        "rating": "rating",
        "budget": "budget",
    }

    data_blocks = infobox.find_all("div", class_="pi-data")

    for block in data_blocks:
        label_tag = block.find("h3", class_="pi-data-label")
        value_tag = block.find("div", class_="pi-data-value")

        if not label_tag or not value_tag:
            continue

        # labels and values sometimes had multiple lines 
        label = clean_text(label_tag.get_text()).lower()
        value = clean_text(value_tag.get_text(" ", strip=True))

        if label in field_map:
            movie_data[field_map[label]] = value

    return movie_data


def scrape_all_movies(movies):
    all_movies_data = []

    for movie in movies:
        # print(f"Scraping: {movie['title']}")
        movie_details = scrape_movie_page(movie["url"])
        if movie_details:
            all_movies_data.append(movie_details)

    return all_movies_data

# commented out sections were for debugging
def main():
    movies = get_movies()
    print(f"\nFound {len(movies)} movies\n")
    # for movie in movies:
    #     print(f"Title: {movie['title']}, URL: {movie['url']}")
    all_movies_data = scrape_all_movies(movies)
    print(f"\nScraped data for {len(all_movies_data)} movies\n")

    with open("marvel_movies.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_movies_data[0].keys())
        writer.writeheader()
        writer.writerows(all_movies_data)
    
    print("\nData written to marvel_movies.csv\n")

main()
