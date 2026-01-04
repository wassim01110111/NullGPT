import traceback

import requests
from bs4 import BeautifulSoup

base_url = "https://lordofthemysteries.fandom.com/wiki/"

error_urls = set()
went_through = set()


def get_category_member(url, info):
    try:
        response = requests.get(base_url + url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", class_="category-page__member-link")

        for link in links:
            if link.has_attr("href"):
                link_href = link["href"].replace("/wiki/", "")
                if link_href not in went_through:
                    print(link_href)
                    went_through.add(link_href)
        next_page = soup.find(
            "a",
            attrs={
                "class": "category-page__pagination-next wds-button wds-is-secondary"
            },
        )
        if next_page and next_page.has_attr("href"):
            next_href = next_page["href"].replace(base_url, "")
            print("next_href found", next_href)
            return get_category_member(next_href, info)
    except Exception as e:
        error_urls.add(url)
        print(f"\n❌ Error while processing URL: {url}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        print("Traceback:")
        traceback.print_exc()


get_category_member("Category:Pathways", {})
