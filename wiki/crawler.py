import json
import traceback
from pathlib import Path

import requests
from bs4 import BeautifulSoup

url_list_path = Path(__file__).resolve().parent / "url_list.json"
end_lotm = 1394
lotm_timestamps = [213, 482, 732, 946, 1150, 1266, 1353, end_lotm]
end_sidestories = 1445
end_coi = end_sidestories + 1179
coi_timestamps = [
    end_sidestories + 109,
    end_sidestories + 263,
    end_sidestories + 494,
    end_sidestories + 735,
    end_sidestories + 884,
    end_sidestories + 1034,
    end_sidestories + 1115,
    end_coi,
]

base_url = "https://lordofthemysteries.fandom.com/wiki/"
url_cats = {
    "wechat": {
        "url": "Category:Archived",
        "exact_chapter": end_coi,
        "chapter_range": None,
    },
    "lotm_portal": {
        "url": "Portal:Lord_of_Mysteries",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "coi_portal": {
        "url": "Portal:Circle_of_Inevitability",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "settings": {
        "url": "Category:Settings",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "notes": {
        "url": "Category:Author%27s_Notes/Book_One",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "organizations": {
        "url": "Category:Organizations",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "items": {
        "url": "Category:Items",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "terminology": {
        "url": "Category:Terminology",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "locations": {
        "url": "Category:Location",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "characters": {
        "url": "Category:Characters",
        "exact_chapter": None,
        "chapter_range": None,
    },
    "book_one_content": {
        "url": "Category:Book_One_Content",
        "exact_chapter": end_sidestories,
        "chapter_range": None,
    },
    "book_two_content": {
        "url": "Category:Book_Two_Content",
        "exact_chapter": end_coi,
        "chapter_range": None,
    },
    "alive": {
        "url": "Category:Alive",
        "exact_chapter": end_coi,
        "chapter_range": None,
    },
    "deceased": {
        "url": "Category:Deceased",
        "exact_chapter": end_coi,
        "chapter_range": None,
    },
    "pathways": {
        "url": "Category:Pathways",
        "exact_chapter": end_coi,
        "chapter_range": None,
    },
}

exclusion_urls = set()  # urls that shouldn't get scraped


specific_urls = {
    "An_Ordinary_Person%27s_Daily_Life_(Side_Story)": {
        "exact_chapter": end_sidestories,
        "chapter_range": None,
    },
    "Volume_1:_Clown": {
        "exact_chapter": lotm_timestamps[0],
        "chapter_range": None,
    },
    "Volume_2:_Faceless": {
        "exact_chapter": lotm_timestamps[1],
        "chapter_range": None,
    },
    "Volume_3:_Traveler": {
        "exact_chapter": lotm_timestamps[2],
        "chapter_range": None,
    },
    "Volume_4:_Undying": {
        "exact_chapter": lotm_timestamps[3],
        "chapter_range": None,
    },
    "Volume_5:_Red_Priest": {
        "exact_chapter": lotm_timestamps[4],
        "chapter_range": None,
    },
    "Volume_6:_Lightseeker": {
        "exact_chapter": lotm_timestamps[5],
        "chapter_range": None,
    },
    "Volume_7:_The_Hanged_Man": {
        "exact_chapter": lotm_timestamps[6],
        "chapter_range": None,
    },
    "Volume_8:_Fool": {
        "exact_chapter": lotm_timestamps[7],
        "chapter_range": None,
    },
    "Volume_1:_Nightmare": {
        "exact_chapter": coi_timestamps[0],
        "chapter_range": None,
    },
    "Volume_2:_Lightseeker": {
        "exact_chapter": coi_timestamps[1],
        "chapter_range": None,
    },
    "Volume_3:_Conspirer": {
        "exact_chapter": coi_timestamps[2],
        "chapter_range": None,
    },
    "Volume_4:_Sinner": {
        "exact_chapter": coi_timestamps[3],
        "chapter_range": None,
    },
    "Volume_5:_Demoness": {
        "exact_chapter": coi_timestamps[4],
        "chapter_range": None,
    },
    "Volume_6:_Dream_Weaver": {
        "exact_chapter": coi_timestamps[5],
        "chapter_range": None,
    },
    "Volume_7:_Second_Law": {
        "exact_chapter": coi_timestamps[6],
        "chapter_range": None,
    },
    "Volume_8:_Eternal_Aeon": {
        "exact_chapter": coi_timestamps[7],
        "chapter_range": None,
    },
    'Bilibili_LOTM-related_Content_Creator_"Chu_Zhaolan"_-_100,000_subscriber_special_video_-_I%27ve_interviewed_Cuttlefish': {
        "exact_chapter": coi_timestamps[5],
        "chapter_range": None,
    },
}
# keeping track of the urls scraped to avoid duplicates and time loss
went_through = set()
error_urls = set()
with open(url_list_path, "r", encoding="utf-8") as f:
    url_list = json.load(f) | specific_urls


def url_list_update(url, info):
    url_list[url] = info


def get_category_member(url, info):
    print(f"Going through {url}")
    try:
        response = requests.get(base_url + url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", class_="category-page__member-link")

        for link in links:
            if link.has_attr("href"):
                link_href = link["href"].replace("/wiki/", "")
                if link_href not in went_through:
                    went_through.add(link_href)
                    if link_href.startswith("Category:"):
                        get_category_member(url=link_href, info=info)
                    else:
                        url_list_update(url=link_href, info=info)

        next_page = soup.find(
            "a",
            attrs={
                "class": "category-page__pagination-next wds-button wds-is-secondary"
            },
        )
        if next_page and next_page.has_attr("href"):
            next_href = next_page["href"].replace(base_url, "")
            return get_category_member(url=next_href, info=info)

    except Exception as e:
        error_urls.add(url)
        print(f"\n❌ Error while processing URL: {url}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        print("Traceback:")
        traceback.print_exc()


for url in specific_urls:
    went_through.add(url)

for cat in url_cats:
    get_category_member(
        url=url_cats[cat]["url"],
        info={
            "exact_chapter": url_cats[cat]["exact_chapter"],
            "chapter_range": url_cats[cat]["chapter_range"],
        },
    )

with open(url_list_path, "w", encoding="utf-8") as f:
    json.dump(url_list, f, ensure_ascii=False, indent=2)
