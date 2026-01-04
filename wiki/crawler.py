import json
import traceback
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

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
        "exclusions": set(),
    },
    "items": {
        "url": "Category:Items",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "terminology": {
        "url": "Category:Terminology",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "locations": {
        "url": "Category:Location",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "characters": {
        "url": "Category:Characters",
        "exact_chapter": None,
        "chapter_range": None,
        "exclusions": set(),
    },
    "book_one_content": {
        "url": "Category:Book_One_Content",
        "exact_chapter": end_sidestories,
        "chapter_range": None,
        "exclusions": set(),
    },
    "book_two_content": {
        "url": "Category:Book_Two_Content",
        "exact_chapter": end_coi,
        "chapter_range": None,
        "exclusions": set(),
    },
    "alive": {
        "url": "Category:Alive",
        "exact_chapter": end_coi,
        "chapter_range": None,
        "exclusions": set(),
    },
    "deceased": {
        "url": "Category:Deceased",
        "exact_chapter": end_coi,
        "chapter_range": None,
        "exclusions": set(),
    },
    "pathways": {
        "url": "Category:Pathways",
        "exact_chapter": end_coi,
        "chapter_range": None,
        "exclusions": set(),
    },
}

exclusion_urls = set()  # urls that shouldn't get scraped
with open("url_list.json", "r", encoding="utf-8") as f:
    url_list = json.load(f)


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


def url_cleaning(url):
    if url.startswith(base_url):
        url = url[len(base_url) :]
    else:  # for urls that aren't wiki links
        print("not a wiki url", url)

    parsed = urlparse(url)
    return parsed.path


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
                    went_through.add(link_href)

    except Exception as e:
        error_urls.add(url)
        print(f"\n❌ Error while processing URL: {url}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        print("Traceback:")
        traceback.print_exc()
