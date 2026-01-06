import json
import traceback

from bs4 import BeautifulSoup
from crawler import end_sidestories
from pageDL import html_folder, sanitize_filename, url_list_path

not_support_html = set()

DEBUG = True
fake_categories = {"test"}
error_html = set()
soup = None
context_hrefs = {
    "/wiki/Lord_of_Mysteries_(Novel)": 0,
    "/wiki/Circle_of_Inevitability_(Novel)": end_sidestories,
}

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
            unsupported(f"something wrong with this ref {el} 1")
        ref_id = a_tag["href"].lstrip("#")
        li_ref = soup.find("li", id=ref_id)
        ref_span = li_ref.find("span", class_="reference-text")
        ref_source = ref_span.find("a")["href"]
        print(ref_span)
        chapter_span = ref_span.find_all("span")[-1].get_text(strip=True)
        print(chapter_span)
        if ref_source in context_hrefs and chapter_span:
            references.add(
                context_hrefs[ref_source]
                + int("".join(filter(str.isdigit, chapter_span)))
            )
        else:
            print(ref_source, chapter_span)
            unsupported(f"something wrong with this ref {el} 2")
        ref.decompose()
    if references:
        print(el, references)
        input()
    return el, references


def get_headline(h2):
    headline = h2.find("span", class_="mw-headline")
    headline, ref = clean_references(headline)
    return headline.get_text(strip=True), ref


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
                        sub_category, headline_ref = get_headline(el)
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
    page_analysis("Trier")
