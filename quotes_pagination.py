import pandas as pd
from bs4 import BeautifulSoup
import time
import requests



base_url = "http://quotes.toscrape.com/page/{}/"\

data = []
max_pages = 10

for page in range(1, max_pages + 1):
    print(f'Scraping Page {page}...')

    response = requests.get(base_url.format(page))

    if response.status_code != 200:
        print("No more pages found! Stopping...")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    quote_blocks = soup.find_all("div", class_="quote")

    for block in quote_blocks:
        quote = block.find("span", class_="text").text
        author = block.find("small", class_="author").text
        tag_elements = block.find_all("a", class_="tag")
        tags = [tag.text for tag in tag_elements]

        data.append({
            "Quote": quote,
            "Author": author,
            "Tags": ", ".join(tags)
        })

    page += 1

    time.sleep(1)

    df = pd.DataFrame(data)
    df.to_excel("pagination_quotes.xlsx", index=False)

    print("excel sheet was created")
    print(f"Collected {len(data)} quotes so far")