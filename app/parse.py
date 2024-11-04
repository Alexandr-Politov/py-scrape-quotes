import csv
from dataclasses import dataclass, fields, astuple
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


QUOTES_OUTPUT_CSV_FILE = "quotes.csv"
BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]

QUOTE_FIELDS = [field.name for field in fields(Quote)]


def parse_single_quote(quote_soup: BeautifulSoup) -> Quote:
    return Quote(
        text=quote_soup.select_one(".text").text,
        author=quote_soup.select_one(".author").text,
        tags=[tag.get_text() for tag in quote_soup.select(".tags > .tag")]
        )


def get_quotes() -> [Quote]:
    page_content = requests.get(BASE_URL).content
    soup = BeautifulSoup(page_content, "html.parser")

    quotes = soup.select(".quote")

    return [parse_single_quote(quote_soup) for quote_soup in quotes]


def write_quotes_to_csv(quotes: [Quote], output_csv_path: str) -> None:
    with open(output_csv_path, "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(QUOTE_FIELDS)
        writer.writerows([astuple(quote) for quote in quotes])


def main(output_csv_path: str) -> None:
    quotes = get_quotes()
    write_quotes_to_csv(quotes, output_csv_path)


if __name__ == "__main__":
    main(QUOTES_OUTPUT_CSV_FILE)
