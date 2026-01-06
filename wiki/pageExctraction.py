import json
import traceback

from bs4 import BeautifulSoup
from pageDL import html_folder, sanitize_filename, url_list_path

not_support_html = set()

DEBUG = True
fake_categories = {"test"}
error_html = set()
soup = None


with open(url_list_path, "r", encoding="utf-8") as f:
    url_list = json.load(f)


def unsupported(url):
    input(f"{url} is not supported yet")
    not_support_html.add(url)


def paragraph_analysis(paragraph, categories=set()):
    print(categories)
    clean_references(paragraph)
    print(paragraph.get_text().replace("\n", ""))


def find_page_categories(el):
    categories_list = set()

    if el:
        a_tags = el.find_all("a")
        for a in a_tags:
            cat = a.get_text(strip=True)
            if (
                cat
                and cat not in fake_categories
                and "wds-dropdown__toggle" not in a.get("class", [])
            ):
                categories_list.add(cat)
    else:
        unsupported("categories not found")
    return categories_list


def clean_references(el):
    references = set()
    for ref in el.find_all("sup", class_="reference"):
        a_tag = ref.find("a", href=True)
        if not a_tag:
            unsupported(f"something wrong with this ref {el}")
        ref_id = a_tag["href"].lstrip("#")
        li_ref = soup.find("li", id=ref_id)
        ref_span = li_ref.find("span", class_="reference-text")
        input(ref_span.get_text(strip=True))
        ref.decompose()
    return el


def get_headline(h2):
    headline = h2.find("span", class_="mw-headline")
    return clean_references(headline).get_text(strip=True)


def page_analysis(url):
    global soup
    exact_chapter = url_list[url]["exact_chapter"]
    chapter_range = url_list[url]["chapter_range"]
    file_path = html_folder / f"{sanitize_filename(url)}.html"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        containers = soup.find_all("div", class_="mw-content-ltr mw-parser-output")

        if containers:
            main_container = containers[0]
            for aside in main_container.find_all("aside"):
                aside.decompose()
            elements = containers[0].find_all(["h2", "p"], recursive=False)
            categories = find_page_categories(
                soup.find("div", class_="page-header__categories")
            )
            sub_category = None
            for el in elements:
                if el.get_text(strip=True):
                    if el.name == "h2":
                        sub_category = get_headline(el)
                    elif el.name == "p":
                        if sub_category:
                            paragraph_analysis(
                                el, categories=categories | {sub_category}
                            )
                        else:
                            paragraph_analysis(el, categories=categories)
        else:
            unsupported(url)

    except Exception as e:
        error_html.add(url)
        print(f"\n❌ Error while processing URL: {url}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        print("Traceback:")
        traceback.print_exc()


def main():
    total = len(url_list)

    for i, url in enumerate(url_list, start=1):
        print(url)

        page_analysis(url=url)
        percent = (i / total) * 100
        print(f"Processed {i}/{total} ({percent:.2f}%) - {url}")


if __name__ == "__main__":
    page_analysis("Roselle_Gustav")
